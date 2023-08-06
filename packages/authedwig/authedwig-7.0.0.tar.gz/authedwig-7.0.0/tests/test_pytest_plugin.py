pytest_plugins = ["pytester"]


def test_plugin(testdir):
    # create a temporary pytest test file
    testdir.makepyfile(
        models="""
        from enum import Enum


        class MessageType(Enum):
            trip_created = 'trip_created'
            device_created = 'device.created'
            vehicle_created = 'vehicle_created'
    """
    )

    testdir.makeconftest(
        """
        from enum import Enum

        import pytest

        import hedwig.conf
        from hedwig import models
        from hedwig.models import Message
        from hedwig.testing.factories import MessageFactory

        from models import MessageType


        @pytest.fixture(autouse=True, params=['aws', 'google'])
        def providers(request, settings):
            if request.param == 'aws':
                try:
                    import hedwig.backends.aws

                    settings.HEDWIG_PUBLISHER_BACKEND = 'hedwig.backends.aws.AWSSNSPublisherBackend'
                    settings.HEDWIG_CONSUMER_BACKEND = 'hedwig.backends.aws.AWSSQSConsumerBackend'
                except ImportError:
                    pytest.skip("AWS backend not importable")

            if request.param == 'google':
                try:
                    import hedwig.backends.gcp

                    settings.GOOGLE_APPLICATION_CREDENTIALS = "DUMMY_GOOGLE_APPLICATION_CREDENTIALS"
                    settings.HEDWIG_PUBLISHER_BACKEND = "hedwig.backends.gcp.GooglePubSubPublisherBackend"
                    settings.HEDWIG_CONSUMER_BACKEND = "hedwig.backends.gcp.GooglePubSubConsumerBackend"
                    settings.GOOGLE_CLOUD_PROJECT = "DUMMY_PROJECT_ID"
                    settings.GOOGLE_PUBSUB_READ_TIMEOUT_S = 5
                except ImportError:
                    pytest.skip("Google backend not importable")

        @pytest.fixture(name='message_type')
        def _message_type():
            return MessageType.trip_created

        @pytest.fixture(name='message_data')
        def _message_data(message_type):
            return MessageFactory.build(msg_type=message_type)

        @pytest.fixture
        def message(message_data):
            return Message(message_data)

        @pytest.fixture(name='other_message_data')
        def _other_message_data(message_type):
            return MessageFactory.build(msg_type=message_type)

        @pytest.fixture
        def settings():
            overrides = {}
            original_module = hedwig.conf.settings._user_settings

            class Wrapped:
                def __getattr__(self, name):
                    return overrides.get(name, getattr(original_module, name))

            hedwig.conf.settings._user_settings = Wrapped()
            hedwig.conf.settings.clear_cache()
            # in case a test overrides HEDWIG_DATA_VALIDATOR_CLASS
            models._validator = None

            try:
                yield hedwig.conf.settings._user_settings
            finally:
                hedwig.conf.settings._user_settings = original_module
                hedwig.conf.settings.clear_cache()
                # in case a test overrides HEDWIG_DATA_VALIDATOR_CLASS
                models._validator = None
    """
    )

    # create a temporary pytest test file
    testdir.makepyfile(
        """
        from models import MessageType


        def test_mock_hedwig_publish_no_publish(settings, mock_hedwig_publish, message_type):
            # check with enum message type
            mock_hedwig_publish.assert_message_not_published(message_type)


        def test_mock_hedwig_publish_publish_check(mock_hedwig_publish, message):
            message.publish()
            # check with enum message type
            mock_hedwig_publish.assert_message_not_published(MessageType.device_created)


        def test_mock_hedwig_publish_publish_check_same_type(mock_hedwig_publish, message, other_message_data):
            message.publish()
            # check with string message type
            mock_hedwig_publish.assert_message_not_published(message.type, data=other_message_data)
            mock_hedwig_publish.assert_message_published(
                message.type, data=message.data, version=message.data_schema_version)


        def test_mock_hedwig_publish_published(mock_hedwig_publish, message):
            message.publish()
            mock_hedwig_publish.assert_message_published(
                message.type, data=message.data, version=message.data_schema_version)


        def test_mock_hedwig_publish_published_without_checking_data(mock_hedwig_publish, message):
            message.publish()
            mock_hedwig_publish.assert_message_published(message.type, version=message.data_schema_version)
    """
    )

    # run all tests with pytest
    result = testdir.runpytest().parseoutcomes()

    # check that all tests passed
    assert result.get('passed', 0) + result.get('skipped', 0) == 10
