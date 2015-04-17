from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
import unittest
import qdatum


class TestClient(unittest.TestCase):

    def setUp(self):
        self.client = qdatum.Client()

    def test_connect(self):
        rsp = self.client.about()
        self.assertDictEqual(rsp, {'version': '0.3.1'})


if __name__ == '__main__':
    unittest.main()
