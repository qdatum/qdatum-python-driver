from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import str
from future import standard_library
standard_library.install_aliases()
from builtins import object
import msgpack
import datetime
import decimal
import logging
import types

logger = logging.getLogger(__name__)


class Pusher(object):
    QUEUE_SIZE = 32

    def __init__(self, driver, feed_id=None):
        self._feed_id = feed_id
        self._driver = driver
        self._session = self._driver.session

    def push(self, data, mime=None):
        if mime is None:
            mime = 'application/x-msgpack'
            payload = self.__iter_generator(data, mime)
        else:
            payload = data
        return self._session.put('/push/' + str(self._feed_id), payload, mime=mime)

    def push_sample(self, data, mime=None):
        if mime is None:
            mime = 'application/x-msgpack'
            payload = self.__iter_generator(data, mime)
        else:
            payload = data
        return self._session.put('/push/sample', payload, mime=mime)

    def insert(self, data):
        return self._session.put('/insert/' + str(self._feed_id), msgpack.packb(data, default=self.__pack_parser, use_bin_type=True), mime="application/x-msgpack")

    def insert_async(self, data):
        return self._session.put_async('/insert/' + str(self._feed_id), msgpack.packb(data, default=self.__pack_parser, use_bin_type=True), mime="application/x-msgpack")

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        del self._session

    @staticmethod
    def __pack_parser(obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y%m%dT%H:%M:%S.%f")
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return obj

    def __iter_generator(self, data, mime):
        logger.info('Reading push payload')
        if hasattr(data, '__call__'):
            for row in data():
                yield msgpack.packb(row, default=self.__pack_parser, use_bin_type=True)
        else:
            yield msgpack.packb(data, default=self.__pack_parser, use_bin_type=True)
