import os
import json
import requests
from tornado.httpclient import AsyncHTTPClient
from tornado.testing import AsyncTestCase, main


class IndexHandlerTestCase(AsyncTestCase):

    def setUp(self):
        super(AsyncTestCase, self).setUp()
        self.io_loop = self.get_new_ioloop()
        self.io_loop.make_current()

        client = AsyncHTTPClient()
        self.fetch = client.fetch
        self.url = 'http://localhost:8205/api/v1/projects'

    def test_index_get(self):
        self.fetch(self.url, self.stop)
        response = self.wait()
        res = json.loads(response.body)
        self.assertIn("count", res)
        self.assertEqual(200, response.code)
        self.assertTrue(isinstance(res, dict))


class ProjectsHandlerTestCase(AsyncTestCase):

    def setUp(self):
        super(AsyncTestCase, self).setUp()
        self.io_loop = self.get_new_ioloop()
        self.io_loop.make_current()
        client = AsyncHTTPClient()
        self.fetch = client.fetch
        self.url = 'http://localhost:8205/api/v1/projects'
        self.basedir = os.path.dirname(os.path.abspath(__file__))
        self.headers = {'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwidXNlcm5hbWUiOiJnYW5uaWN1cyIsImV4cCI6MTU1MDMyMzY3MX0.LeVaHFMM7Z3GPRtzvzQ3tUr2HTuiDnLs4AHC76voxBc'}

    def test_projects_get(self):
        self.fetch(self.url, self.stop)
        response = self.wait()
        res = json.loads(response.body)
        self.assertIn("count", res)
        self.assertEqual(200, response.code)
        self.assertTrue(isinstance(res, dict))

    def test_projects_post(self):
        eggs = {'eggs': open(os.path.join(self.basedir, 'output.egg'), 'rb')}
        pos = {'project': 'arts', 'ssp': False}
        response = requests.post(self.url, data=pos, files=eggs)
        res = json.loads(response.text)
        self.assertEqual(201, response.status_code)
        self.assertIn('arts', response.text)
        self.assertTrue(isinstance(res, dict))

#
# class TestMathFunc(unittest.TestCase):
#
#
#     # TestCase基类方法,所有case执行之前自动执行
#     @classmethod
#     def setUpClass(cls):
#         print("这里是所有测试用例前的准备工作")
#
#     # TestCase基类方法,所有case执行之后自动执行
#     @classmethod
#     def tearDownClass(cls):
#         print("这里是所有测试用例后的清理工作")
#
#     # TestCase基类方法,每次执行case前自动执行
#     def setUp(self):
#         print("这里是一个测试用例前的准备工作")
#
#     # TestCase基类方法,每次执行case后自动执行
#     def tearDown(self):
#         print("这里是一个测试用例后的清理工作")
#
#     @unittest.skip("我想临时跳过这个测试用例.")
#     def test_add(self):
#         self.assertEqual(3, add(1, 2))
#         self.assertNotEqual(3, add(2, 2))  # 测试业务方法add
#
#     def test_minus(self):
#         self.skipTest('跳过这个测试用例')
#         self.assertEqual(1, minus(3, 2))  # 测试业务方法minus
#
#     def test_multi(self):
#         self.assertEqual(6, multi(2, 3))  # 测试业务方法multi
#
#     def test_divide(self):
#         self.assertEqual(2, divide(6, 3))  # 测试业务方法divide
#         self.assertEqual(2.5, divide(5, 2))


if __name__ == '__main__':
    main(verbosity=1)
