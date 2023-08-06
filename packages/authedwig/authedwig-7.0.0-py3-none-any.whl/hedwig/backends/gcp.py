from concurrent.futures import Future
from contextlib import contextmanager, ExitStack
import json
import logging
from datetime import datetime, timezone
from queue import Queue, Empty
import threading
from typing import List, Optional, Mapping, Union, cast, Generator
from unittest import mock

from google.api_core.exceptions import DeadlineExceeded
from google.auth import environment_vars as google_env_vars, default as google_auth_default
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.proto.pubsub_pb2 import ReceivedMessage
from google.cloud.pubsub_v1.subscriber.message import Message as PubSubMessage
from google.cloud.pubsub_v1.types import FlowControl

from hedwig.backends.base import HedwigPublisherBaseBackend, HedwigConsumerBaseBackend
from hedwig.backends.utils import override_env
from hedwig.conf import settings
from hedwig.models import Message


logger = logging.getLogger(__name__)

# the default visibility timeout
# ideally find by calling PubSub REST API
DEFAULT_VISIBILITY_TIMEOUT_S = 20


@contextmanager
def _seed_credentials() -> Generator[None, None, None]:
    """
    Seed environment with explicitly set credentials. Normally we'd stay away from mucking with environment vars,
    however the logic to decode `GOOGLE_APPLICATION_CREDENTIALS` isn't simple, so we let Google libraries handle it.
    """
    with ExitStack() as stack:
        if settings.GOOGLE_APPLICATION_CREDENTIALS:
            stack.enter_context(override_env(google_env_vars.CREDENTIALS, settings.GOOGLE_APPLICATION_CREDENTIALS))

        if settings.GOOGLE_CLOUD_PROJECT:
            stack.enter_context(override_env(google_env_vars.PROJECT, settings.GOOGLE_CLOUD_PROJECT))

        yield


def _auto_discover_project() -> None:
    """
    Auto discover Google project id from credentials. If project id is explicitly set, just use that.
    """
    if not settings.GOOGLE_CLOUD_PROJECT:
        # discover project from credentials
        # there's no way to get this from the Client objects, so we reload the credentials
        _, project = google_auth_default()
        assert project, "couldn't discover project"
        setattr(settings, 'GOOGLE_CLOUD_PROJECT', project)


def get_google_cloud_project() -> str:
    if not settings.GOOGLE_CLOUD_PROJECT:
        with _seed_credentials():
            _auto_discover_project()
    return settings.GOOGLE_CLOUD_PROJECT


# TODO move to dataclasses in py3.7
class GoogleMetadata:
    """
    Google Pub/Sub specific metadata for a Message
    """

    def __init__(self, ack_id: str, subscription_path: str, publish_time: datetime, delivery_attempt: int):
        self._ack_id: str = ack_id
        self._subscription_path: str = subscription_path
        self._publish_time: datetime = publish_time
        self._delivery_attempt = delivery_attempt

    @property
    def ack_id(self) -> str:
        """
        The ID used to ack the message
        """
        return self._ack_id

    @property
    def subscription_path(self) -> str:
        """
        Path of the Pub/Sub subscription from which this message was pulled
        """
        return self._subscription_path

    @property
    def publish_time(self) -> datetime:
        """
        Time this message was originally published to Pub/Sub
        """
        return self._publish_time

    @property
    def delivery_attempt(self) -> int:
        """
        The delivery attempt counter received from Pub/Sub.
        The first delivery of a given message will have this value as 1. The value
        is calculated at best effort and is approximate.
        """
        return self._delivery_attempt

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, GoogleMetadata):
            return False

        return (
            self.ack_id == o.ack_id
            and self.subscription_path == o.subscription_path  # noqa: W503
            and self.delivery_attempt == o.delivery_attempt  # noqa: W503
        )

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return (
            'GoogleMetadata('
            f'ack_id={self.ack_id}, subscription_path={self.subscription_path}, publish_time={self.publish_time}, '
            f'delivery_attempt={self.delivery_attempt}'
            ')'
        )

    def __hash__(self) -> int:
        return hash((self.ack_id, self.subscription_path, self.publish_time))


class GooglePubSubAsyncPublisherBackend(HedwigPublisherBaseBackend):
    def __init__(self) -> None:
        self._publisher = None

    @property
    def publisher(self):
        if self._publisher is None:
            with _seed_credentials():
                self._publisher = pubsub_v1.PublisherClient(batch_settings=settings.HEDWIG_PUBLISHER_GCP_BATCH_SETTINGS)
        return self._publisher

    def publish_to_topic(self, topic_path: str, data: bytes, attrs: Optional[Mapping] = None) -> Union[str, Future]:
        """
        Publishes to a Google Pub/Sub topic and returns a future that represents the publish API call. These API calls
        are batched for better performance.

        Note: despite the signature this doesn't return an actual instance of Future class, but an object that conforms
        to Future class. There's no generic type to represent future objects though.
        """
        attrs = attrs or {}
        attrs = dict((str(key), str(value)) for key, value in attrs.items())
        return self.publisher.publish(topic_path, data=data, **attrs)

    def _get_topic_path(self, message: Message) -> str:
        return self.publisher.topic_path(get_google_cloud_project(), f'hedwig-{message.topic}')

    def _mock_queue_message(self, message: Message) -> mock.Mock:
        gcp_message = mock.Mock()
        gcp_message.message = mock.Mock()
        gcp_message.message.data = json.dumps(message.as_dict()).encode('utf8')
        gcp_message.message.publish_time = datetime.now(timezone.utc)
        gcp_message.ack_id = 'test-receipt'
        return gcp_message

    def _publish(self, message: Message, payload: str, headers: Optional[Mapping] = None) -> Union[str, Future]:
        topic_path = self._get_topic_path(message)
        return self.publish_to_topic(topic_path, payload.encode('utf8'), headers)


class GooglePubSubPublisherBackend(GooglePubSubAsyncPublisherBackend):
    def publish_to_topic(self, topic_path: str, data: bytes, attrs: Optional[Mapping] = None) -> Union[str, Future]:
        return cast(Future, super().publish_to_topic(topic_path, data, attrs)).result()


class MessageWrapper:
    def __init__(self, message: PubSubMessage, subscription_path: str):
        self._message = message
        self._subscription_path = subscription_path

    @property
    def message(self) -> PubSubMessage:
        return self._message

    @property
    def subscription_path(self) -> str:
        return self._subscription_path


class PubSubMessageScheduler:
    """
    A scheduler to use with streaming pull that simply queues all messages for the main thread to pick them up.
    """

    def __init__(self, work_queue: Queue, subscription_path: str):
        self._queue: Queue = Queue()
        self._work_queue: Queue = work_queue
        self._subscription_path: str = subscription_path

    @property
    def queue(self) -> Queue:
        """Queue: A thread-safe queue used for communication between callbacks
        and the scheduling thread."""
        return self._queue

    def schedule(self, callback, message: PubSubMessage) -> None:
        # callback is unused since we never set it in pull_messages
        self._work_queue.put(MessageWrapper(message, self._subscription_path))

    def shutdown(self) -> None:
        """Shuts down the scheduler and immediately end all pending callbacks.
        """
        # ideally we'd nack the messages in work queue, but that might take some time to finish.
        # instead, it's faster to actually process all the messages


class GooglePubSubConsumerBackend(HedwigConsumerBaseBackend):
    def __init__(self, dlq=False) -> None:
        self._subscriber: pubsub_v1.SubscriberClient = None
        self._publisher: pubsub_v1.PublisherClient = None

        if not settings.HEDWIG_SYNC:
            cloud_project = get_google_cloud_project()

            self._subscription_paths: List[str] = []
            if dlq:
                self._subscription_paths = [
                    pubsub_v1.SubscriberClient.subscription_path(cloud_project, f'hedwig-{settings.HEDWIG_QUEUE}-dlq')
                ]
            else:
                self._subscription_paths = [
                    pubsub_v1.SubscriberClient.subscription_path(cloud_project, f'hedwig-{settings.HEDWIG_QUEUE}-{x}')
                    for x in settings.HEDWIG_SUBSCRIPTIONS
                ]
                # main queue for DLQ re-queued messages
                self._subscription_paths.append(
                    pubsub_v1.SubscriberClient.subscription_path(cloud_project, f'hedwig-{settings.HEDWIG_QUEUE}')
                )
            self._dlq_topic_path: str = pubsub_v1.PublisherClient.topic_path(
                cloud_project, f'hedwig-{settings.HEDWIG_QUEUE}-dlq'
            )

    @property
    def subscriber(self):
        if self._subscriber is None:
            with _seed_credentials():
                self._subscriber = pubsub_v1.SubscriberClient()
        return self._subscriber

    @property
    def publisher(self):
        if self._publisher is None:
            with _seed_credentials():
                self._publisher = pubsub_v1.PublisherClient()
        return self._publisher

    def pull_messages(
        self, num_messages: int = 10, visibility_timeout: int = None, shutdown_event: Optional[threading.Event] = None
    ) -> Union[Generator, List]:
        """
        Pulls messages from PubSub subscriptions, using streaming pull, limiting to num_messages messages at a time
        """
        assert self._subscription_paths, "no subscriptions path: ensure HEDWIG_SUBSCRIPTIONS is set"

        if not shutdown_event:
            shutdown_event = threading.Event()

        work_queue: Queue = Queue()
        futures: List[Future] = []
        flow_control: FlowControl = FlowControl(
            max_messages=num_messages, max_lease_duration=visibility_timeout or DEFAULT_VISIBILITY_TIMEOUT_S
        )

        for subscription_path in self._subscription_paths:
            # need a separate scheduler per subscription since the queue is tied to subscription path
            scheduler: PubSubMessageScheduler = PubSubMessageScheduler(work_queue, subscription_path)
            futures.append(
                self.subscriber.subscribe(
                    subscription_path, callback=None, flow_control=flow_control, scheduler=scheduler
                )
            )

        while not shutdown_event.is_set():
            try:
                message = work_queue.get(timeout=1)
                yield message
            except Empty:
                pass

        for future in futures:
            future.cancel()

        # drain the queue
        try:
            while True:
                yield work_queue.get(block=False)
        except Empty:
            pass

    def process_message(self, queue_message: MessageWrapper) -> None:
        self.message_handler(
            queue_message.message.data.decode(),
            GoogleMetadata(
                queue_message.message.ack_id,
                queue_message.subscription_path,
                queue_message.message.publish_time,
                queue_message.message.delivery_attempt,
            ),
        )

    def ack_message(self, queue_message: MessageWrapper) -> None:
        queue_message.message.ack()

    def nack_message(self, queue_message: MessageWrapper) -> None:
        logging.info("nacking message")
        queue_message.message.nack()

    @staticmethod
    def pre_process_hook_kwargs(queue_message: MessageWrapper) -> dict:
        return {'google_pubsub_message': queue_message.message}

    @staticmethod
    def post_process_hook_kwargs(queue_message: MessageWrapper) -> dict:
        return {'google_pubsub_message': queue_message.message}

    def extend_visibility_timeout(self, visibility_timeout_s: int, metadata: GoogleMetadata) -> None:
        """
        Extends visibility timeout of a message on a given priority queue for long running tasks.
        """
        if visibility_timeout_s < 0 or visibility_timeout_s > 600:
            raise ValueError("Invalid visibility_timeout_s")
        self.subscriber.modify_ack_deadline(metadata.subscription_path, [metadata.ack_id], visibility_timeout_s)

    def requeue_dead_letter(self, num_messages: int = 10, visibility_timeout: int = None) -> None:
        """
        Re-queues everything in the Hedwig DLQ back into the Hedwig queue.

        :param num_messages: Maximum number of messages to fetch in one call. Defaults to 10.
        :param visibility_timeout: The number of seconds the message should remain invisible to other queue readers.
        Defaults to None, which is queue default
        """
        topic_path = pubsub_v1.PublisherClient.topic_path(get_google_cloud_project(), f'hedwig-{settings.HEDWIG_QUEUE}')
        assert len(self._subscription_paths) == 1, "multiple subscriptions found"
        subscription_path = self._subscription_paths[0]

        logging.info("Re-queueing messages from {} to {}".format(subscription_path, topic_path))
        while True:
            try:
                queue_messages: List[ReceivedMessage] = self.subscriber.pull(
                    subscription_path, num_messages, retry=None, timeout=settings.GOOGLE_PUBSUB_READ_TIMEOUT_S
                ).received_messages
            except DeadlineExceeded:
                break

            if not queue_messages:
                break

            logging.info("got {} messages from dlq".format(len(queue_messages)))
            for queue_message in queue_messages:
                try:
                    if visibility_timeout:
                        self.subscriber.modify_ack_deadline(
                            subscription_path, [queue_message.ack_id], visibility_timeout
                        )

                    future = self.publisher.publish(
                        topic_path, data=queue_message.message.data, **queue_message.message.attributes
                    )
                    # wait for success
                    future.result()
                    logger.debug(
                        'Re-queued message from DLQ {} to {}'.format(subscription_path, topic_path),
                        extra={'message_id': queue_message.message.message_id},
                    )

                    self.subscriber.acknowledge(subscription_path, [queue_message.ack_id])
                except Exception:
                    logger.exception('Exception in requeue message from {} to {}'.format(subscription_path, topic_path))

            logging.info("Re-queued {} messages".format(len(queue_messages)))
