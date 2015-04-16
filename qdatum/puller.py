import msgpack
import logging

logger = logging.getLogger(__name__)


class Puller():
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
