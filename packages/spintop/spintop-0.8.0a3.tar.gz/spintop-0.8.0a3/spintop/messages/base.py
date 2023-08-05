from functools import wraps
from collections import defaultdict

from .models import TestsUpdateMessage
from .models import TestsUpdateQueryMessage

from .schemas import get_schema

TESTS_UPDATE_TOPIC = 'tests.update'
TESTS_UPDATE_QUERY_TOPIC = 'tests.update_query'

def messages_endpoint(topic_name, message_model_cls):
    return property(
        fget = lambda publisher: _MessagesEndpoint(publisher, topic_name, message_model_cls)
    )

class SpintopMessagePublisher(object):
    tests_update = messages_endpoint(TESTS_UPDATE_TOPIC, TestsUpdateMessage)
    tests_query_update = messages_endpoint(TESTS_UPDATE_QUERY_TOPIC, TestsUpdateQueryMessage)

    def subscribe(self, topic, callback):
        raise NotImplementedError()

    def publish(self, topic, message):
        raise NotImplementedError()

    def prepare_message(self, message):
        pass

    def supports_publish(self):
        return True

    def supports_subscribe(self):
        return True

class _MessagesEndpoint(object):
    def __init__(self, publisher, topic, message_model_cls):
        self.publisher = publisher
        self.topic = topic
        self.message_model_cls = message_model_cls
    
    @property
    def schema(self):
        return get_schema(self.message_model_cls)

    def subscribe(self, callback):
        if self.publisher.supports_subscribe():
            @wraps(callback)
            def _wrapper(raw_message):
                message = self.load_message(raw_message)
                callback(message)

            self.publisher.subscribe(self.topic, _wrapper)

    def dump_message(self, message):
        return self.schema.dump(message)

    def load_message(self, raw_message):
        return self.schema.load(raw_message)

    def publish(self, message):
        if self.publisher.supports_publish():
            self.publisher.prepare_message(message)
            content = self.dump_message(message)
            self.publisher.publish(self.topic, content)

class LocalMessagePublisher(SpintopMessagePublisher):
    def __init__(self, local_env):
        self._local_subscribers = defaultdict(list)
        self._env = local_env

    def subscribe(self, topic, callback):
        self._local_subscribers[topic].append(callback)

    def publish(self, topic, message):
        self._publish(topic, message)
        self._notify_local(topic, message)

    def prepare_message(self, message):
        message.env = self._env.freeze_database_access_only()
        super().prepare_message(message)

    def _notify_local(self, topic, message):
        for subscriber in self._local_subscribers[topic]:
            subscriber(message)

    def _publish(self, topic, message):
        pass

class NoopMessagePublisher(SpintopMessagePublisher):
    
    def supports_publish(self):
        return False

    def supports_subscribe(self):
        return False