import json

from .errors import *
from .driver import Driver
from qdatum.pusher import Pusher
from qdatum.puller import Puller

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


"""
A collection of common routes on the API
"""


class Client(Driver):

    def register(self, entity, user):
        entity = json_force(entity)
        entity['user'] = json_force(user)
        return self.query('/entity').post(entity)

    def get_endpoints(self):
        return self.query('/').get()

    def about(self):
        return self.query('/about').get()

    @Driver._authenticated
    def get_feed(self, id):
        return self.query('/feed/' + str(id)).get()

    @Driver._authenticated
    def get_feeds(self, **kwargs):
        return self.query('/feeds').post(kwargs)

    @Driver._authenticated
    def create_feed(self, obj):
        return self.query('/feed').post(obj)

    @Driver._authenticated
    def update_feed(self, id, obj):
        return self.query('/feed/' + str(id)).post(obj)

    @Driver._authenticated
    def create_tap(self, obj):
        return self.query('/tap').post(obj)

    @Driver._authenticated
    def update_tap(self, id, obj):
        return self.query('/tap/' + str(id)).post(obj)

    @Driver._authenticated
    def push(self, id, payload, mime=None):
        pusher = Pusher(id, payload, mime=mime)
        return self.query('/push/' + str(id)).put_stream(pusher)

    @Driver._authenticated
    def apply(self, tap_id):
        return self.query('/tap/' + str(tap_id) + '/apply').get()

    @Driver._authenticated
    def approve(self, subscription_id):
        return self.query('/subscription/' + str(subscription_id) + '/approve').get()

    @Driver._authenticated
    def reject(self, subscription_id):
        return self.query('/subscription/' + str(subscription_id) + '/reject').get()

    @Driver._authenticated
    def pull(self, id):
        return Puller(self.query('/pull/' + str(id), stream=True).get(format='msgpack'))

    @Driver._authenticated
    def get_flows(self, **args):
        return self.query('/flows').post(args)
