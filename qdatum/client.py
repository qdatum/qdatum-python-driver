import json

from .errors import *
from .driver import Driver
from .pusher import Pusher

__all__ = [
    "Client"
]


def json_force(value):
    if isinstance(value, str):
        return json.loads(value)
    elif isinstance(value, dict):
        return value
    else:
        return dict(value)


class Client(Driver):

    def register(self, entity, user):
        entity = json_force(entity)
        entity['user'] = json_force(user)
        return self.query('/entity').post(entity)

    @BaseClient._authenticated
    def get_feed(self, id):
        return self.query('/feed/' + str(id)).get()

    @BaseClient._authenticated
    def get_feeds(self, opt=None):
        return self.query('/feeds').get()

    @BaseClient._authenticated
    def create_feed(self, obj):
        return self.query('/feed').post(obj)

    @BaseClient._authenticated
    def update_feed(self, id, obj):
        return self.query('/feed/' + str(id)).post(obj)

    @BaseClient._authenticated
    def create_tap(self, obj):
        return self.query('/tap').post(obj)

    @BaseClient._authenticated
    def update_tap(self, id, obj):
        return self.query('/tap/' + str(id)).post(obj)

    @BaseClient._authenticated
    def push(self, id, payload):
        pusher = Pusher(id, payload)
        return self.query('/push/' + str(id)).put_stream(pusher)

    @BaseClient._authenticated
    def apply(self, tap_id):
        return self.query('/tap/' + str(tap_id) + '/apply').get()

    @BaseClient._authenticated
    def approve(self, subscription_id):
        return self.query('/subscription/' + str(subscription_id) + '/approve').get()

    @BaseClient._authenticated
    def reject(self, subscription_id):
        return self.query('/subscription/' + str(subscription_id) + '/reject').get()

    @BaseClient._authenticated
    def pull(self, id, params={'format': 'csv'}, stream=False):
        return self.query('/pull/' + str(id), stream=stream).get(params)
