from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import dict
from builtins import str
from future import standard_library
standard_library.install_aliases()
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
        return self.session.post('/entity', entity)

    def get_endpoints(self):
        return self.session.get('/')

    def about(self):
        return self.session.get('/about')

    @Driver._authenticated
    def get_feed(self, id):
        return self.session.get('/feed/' + str(id))

    @Driver._authenticated
    def get_feeds(self, **kwargs):
        return self.session.post('/feeds/', kwargs)

    @Driver._authenticated
    def create_feed(self, obj):
        return self.session.post('/feed', obj)

    @Driver._authenticated
    def update_feed(self, id, obj):
        return self.session.post('/feed/' + str(id), obj)

    @Driver._authenticated
    def create_tap(self, obj):
        return self.session.post('/tap', obj)

    @Driver._authenticated
    def update_tap(self, id, obj):
        return self.session.post('/tap/' + str(id), obj)

    @Driver._authenticated
    def get_pusher(self, feed_id):
        return Pusher(self, feed_id)

    @Driver._authenticated
    def apply(self, tap_id):
        return self.session.get('/tap/' + str(tap_id) + '/apply')

    @Driver._authenticated
    def approve(self, subscription_id):
        return self.session.get('/subscription/' + str(subscription_id) + '/approve')

    @Driver._authenticated
    def reject(self, subscription_id):
        return self.session.get('/subscription/' + str(subscription_id) + '/reject')

    @Driver._authenticated
    def pull(self, id):
        return self.session.get('/pull/' + str(id), stream=True, format='msgpack')

    @Driver._authenticated
    def get_flows(self, **kwargs):
        return self.session.post('/flows', kwargs)
