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

from qdatum import errors

logger = logging.getLogger(__name__)


class Puller(object):
    def __init__(self, rsp):
        logger.info('Unpacking pull request')
        self.content = rsp.iter_content()
        self.unpacker = msgpack.Unpacker(encoding='utf-8')
        self.recv_gen = self.__recv()

        #self.unpacker = msgpack.Unpacker(rsp.iter_content(), encoding='utf-8')

    def __recv(self):
        while True:
            buf = next(self.content)
            if not buf:
                break
            self.unpacker.feed(buf)
            for o in self.unpacker:
                yield o

    def __iter__(self):
        return self

    def __next__(self):

        try:
            return next(self.recv_gen)
        except StopIteration:
            raise StopIteration
        except TypeError:
            raise StopIteration

    def readall(self):
        rsp = []
        for row in self:
            rsp.append(row)
        return rsp
