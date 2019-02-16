from tornado.testing import AsyncHTTPSTestCase, AsyncTestCase, main
from tornado.httpclient import AsyncHTTPClient


class IndexHandlerTestCase(AsyncTestCase):

    def test_index_get(self):
        client = AsyncHTTPClient()

        client.fetch('http://localhost:8205/api/v1', self.stop)
        response = self.wait()
        self.assertEqual(200, response.code)


if __name__ == '__main__':
    main(verbosity=2)
