from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import next
from future import standard_library
standard_library.install_aliases()
from builtins import object
import msgpack
import logging

logger = logging.getLogger(__name__)


class Puller(object):
    def __init__(self, rsp):
        logger.info('Unpacking pull request')
        self.unpacker = msgpack.Unpacker(rsp.content, encoding='utf-8')

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return next(self.unpacker)
        except StopIteration:
            raise StopIteration

    def readall(self):
        rsp = []
        for row in self:
            rsp.append(row)
        return rsp
