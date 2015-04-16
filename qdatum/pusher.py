import msgpack
import datetime
import decimal
import logging

logger = logging.getLogger(__name__)


class Pusher():
    def __init__(self, id, payload=None):
        self._payload = payload

    def get_mime(self):
        return 'application/x-msgpack'

    @staticmethod
    def __pack_parser(obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y%m%dT%H:%M:%S.%f")
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return obj

    def read(self):
        logger.info('Reading push payload')
        if hasattr(self._payload, '__call__'):
            for row in self._payload():
                yield msgpack.packb(row, default=self.__pack_parser, use_bin_type=True)
        else:
            yield msgpack.packb(self._payload(), default=self.__pack_parser, use_bin_type=True)