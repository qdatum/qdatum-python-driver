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
