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

logger = logging.getLogger(__name__)


class Pusher(object):
    def __init__(self, id, payload=None, mime="application/x-msgpack"):
        self._payload = payload
        self._mime = mime

    def get_mime(self):
        return self.mime

    @staticmethod
    def __pack_parser(obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y%m%dT%H:%M:%S.%f")
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return obj

    def get_payload(self):
        return self._payload

    def read(self):
        logger.info('Reading push payload')

        if hasattr(self._payload, '__call__'):
            for row in self._payload():
                yield msgpack.packb(row, default=self.__pack_parser, use_bin_type=True)
        else:
            yield msgpack.packb(self._payload, default=self.__pack_parser, use_bin_type=True)
