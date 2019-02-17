import os
import json
import requests
import unittest


class IndexHandlerTestCase(unittest.TestCase):

    def setUp(self):
        self.url = 'http://localhost:8205/api/v1/projects'

    def test_index_handler_get(self):
        resp = requests.get(self.url)
        self.assertEqual(200, resp.status_code)
        self.assertIn("count", resp.text)
        self.assertNotEqual("successful", resp.text)
        self.assertTrue(isinstance(json.loads(resp.text), dict))


class ProjectsHandlerTestCase(unittest.TestCase):

    def setUp(self):
        self.project = 'arts'
        self.spider = 'tips'
        self.ssp = False
        self.url = 'http://localhost:8205/api/v1/projects'
        self.basedir = os.path.dirname(os.path.abspath(__file__))
        self.headers = {'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwidXNlcm5hbWUiOiJnYW5uaWN1cyIsImV4cCI6MTU1MDMyMzY3MX0.LeVaHFMM7Z3GPRtzvzQ3tUr2HTuiDnLs4AHC76voxBc'}

    def test_projects_handler_get(self):
        # Testing APIs without parameters
        resp = requests.get(self.url, headers=self.headers)
        self.assertEqual(200, resp.status_code)
        self.assertIn("count", resp.text)
        self.assertIn("results", resp.text)
        self.assertNotEqual("successful", resp.text)
        self.assertTrue(isinstance(json.loads(resp.text), dict))

        # Testing API with the right parameters
        custom_url = self.url + '?ordering=-id&offset=1&ssp=1'
        resp2 = requests.get(custom_url, headers=self.headers)
        self.assertEqual(200, resp2.status_code)
        self.assertIn("count", resp2.text)
        self.assertIn("results", resp2.text)
        self.assertNotEqual("successful", resp2.text)
        self.assertTrue(isinstance(json.loads(resp2.text), dict))

        # Testing API with the incorrect parameters
        custom_url2 = self.url + '?ordering=a&offset=a&wrong=a'
        resp3 = requests.get(custom_url2, headers=self.headers)
        self.assertNotEqual(200, resp3.status_code)

    def test_projects_handler_post(self):
        # Testing API with the right parameters
        eggs = {'eggs': open(os.path.join(self.basedir, 'output.egg'), 'rb')}
        pos = {'project': self.project, 'ssp': self.ssp}
        resp = requests.post(self.url, data=pos, files=eggs, headers=self.headers)
        self.assertEqual(201, resp.status_code)
        self.assertIn('arts', resp.text)
        self.assertTrue(isinstance(json.loads(resp.text), dict))

        # Testing API with the incorrect file type
        files = {'eggs': open(os.path.join(self.basedir, 'lol.jpg'), 'rb')}
        pos2 = {'project': self.project, 'ssp': self.ssp}
        resp2 = requests.post(self.url, data=pos2, files=files, headers=self.headers)
        self.assertEqual(400, resp2.status_code)

        # Testing API with the incorrect parameters
        eggs3 = {'eggs': open(os.path.join(self.basedir, 'output.egg'), 'rb')}
        pos3 = {'ssp': self.ssp}
        resp3 = requests.post(self.url, data=pos3, files=eggs3, headers=self.headers)
        self.assertEqual(400, resp3.status_code)

    @unittest.skip('Delete tests should ensure that records exist in the database.')
    def test_projects_handler_delete(self):
        # The project name and id and version from sqlite. Please prepare the data before testing
        params_url = self.url + '?id=5' + '&project=' + self.project + '&version=1550297128'
        resp = requests.delete(params_url, headers=self.headers)
        self.assertIn('successful', resp.text)
        self.assertEqual(200, resp.status_code)
        self.assertIn(self.project, resp.text)

        self.assertNotEqual('failed', resp.text)


class SchedulerHandlerTestCase(unittest.TestCase):

    def setUp(self):
        self.project = 'arts'
        self.spider = 'tips'
        self.version = '1550366591'
        self.mode = 'interval'
        self.timer = "{'seconds': 100}"
        self.status = True
        self.ssp = False
        self.url = 'http://localhost:8205/api/v1/schedulers'
        self.headers = {'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwidXNlcm5hbWUiOiJnYW5uaWN1cyIsImV4cCI6MTU1MDMyMzY3MX0.LeVaHFMM7Z3GPRtzvzQ3tUr2HTuiDnLs4AHC76voxBc'}

    def test_schedulers_handler_get(self):
        # Testing API with the right parameters
        resp = requests.get(self.url, headers=self.headers)
        res = json.loads(resp.text)
        self.assertEqual(200, resp.status_code)
        self.assertIn("count", resp.text)
        self.assertIn("current", resp.text)
        self.assertIn("results", resp.text)
        self.assertTrue(isinstance(res, dict))
        self.assertNotEqual(None, len(res['current']))  # scheduler current job default is 2
        self.assertNotEqual("successful", resp.text)
        self.assertNotEqual("failed", resp.text)

        # Testing API with the right parameters
        custom_url = self.url + '?ordering=-id'
        resp2 = requests.get(custom_url, headers=self.headers)
        self.assertEqual(200, resp2.status_code)
        self.assertIn("count", resp2.text)
        self.assertIn("results", resp2.text)
        self.assertNotEqual("successful", resp2.text)
        self.assertTrue(isinstance(json.loads(resp2.text), dict))

        # Testing API with the incorrect parameters
        custom_url2 = self.url + '?ordering=a&offset=a&wrong=a'
        resp3 = requests.get(custom_url2, headers=self.headers)
        self.assertNotEqual(200, resp3.status_code)

    def test_schedulers_handler_post(self):
        # Testing API with the right parameters
        params = {'project': self.project, 'spider': self.spider, 'version': self.version,
                  'ssp': self.ssp, 'mode': self.mode, 'timer': self.timer, 'status': self.status}
        resp = requests.post(self.url, data=params)
        self.assertEqual(201, resp.status_code)
        self.assertIn("project", resp.text)
        self.assertIn("version", resp.text)
        self.assertIn("status", resp.text)
        self.assertIn("successful", resp.text)

        # Testing API with the incorrect parameters
        params['timer'] = 5
        resp2 = requests.post(self.url, data=params)
        self.assertEqual(400, resp2.status_code)
        self.assertIn('error of timer', resp2.text)

    @unittest.skip('The id from sqlite. Please prepare the data before testing')
    def test_schedulers_handler_put(self):
        # Testing API with the right parameters
        params = {'id': 1, 'status': False}
        resp = requests.put(self.url, data=params)
        self.assertIn('successful', resp.text)
        self.assertTrue(200, resp.status_code)

        # Testing API with the incorrect parameters
        params2 = {'status': False}  # id not null
        resp2 = requests.put(self.url, data=params2)
        self.assertTrue(400, resp2.status_code)

    @unittest.skip('The id from sqlite. Please prepare the data before testing')
    def test_schedulers_handler_delete(self):
        # Testing API with the right parameters
        params = {'id': 1}
        resp = requests.put(self.url, data=params)
        self.assertIn('successful', resp.text)
        self.assertIn('project', resp.text)
        self.assertTrue(200, resp.status_code)

        # Testing API with the incorrect parameters
        params2 = {}  # id not null
        resp2 = requests.put(self.url, data=params2)
        self.assertIn('dose not exist', resp2.text)
        self.assertTrue(400, resp2.status_code)


class RecordHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self.url = 'http://localhost:8205/api/v1/records'
        self.headers = {'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwidXNlcm5hbWUiOiJnYW5uaWN1cyIsImV4cCI6MTU1MDMyMzY3MX0.LeVaHFMM7Z3GPRtzvzQ3tUr2HTuiDnLs4AHC76voxBc'}

    def test_record_handler_get(self):
        # Testing API with the right parameters
        resp = requests.get(self.url, headers=self.headers)
        res = json.loads(resp.text)
        self.assertEqual(200, resp.status_code)
        self.assertIn("count", resp.text)
        self.assertIn("results", resp.text)
        self.assertTrue(isinstance(res, dict))
        self.assertNotEqual("successful", resp.text)
        self.assertNotEqual("failed", resp.text)

        # Testing API with the right parameters
        custom_url = self.url + '?ordering=-id'
        resp2 = requests.get(custom_url, headers=self.headers)
        self.assertEqual(200, resp2.status_code)
        self.assertIn("count", resp2.text)
        self.assertIn("results", resp2.text)
        self.assertNotEqual("successful", resp2.text)
        self.assertTrue(isinstance(json.loads(resp2.text), dict))

        # Testing API with the incorrect parameters
        custom_url2 = self.url + '?ordering=a&offset=a&wrong=a'
        resp3 = requests.get(custom_url2, headers=self.headers)
        self.assertNotEqual(200, resp3.status_code)


class RegisterHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self.username1 = 'TestMan'
        self.email1 = 'unittest@python.com'
        self.role1 = 'superuser'

        self.username2 = 'TestMan2'
        self.email2 = 'unittest2@python.com'
        self.role2 = 'observer'

        self.username3 = 'TestMan3'
        self.email3 = 'unittest3@python.com'
        self.role3 = 'wrong'

        self.password = 'admin'
        self.url = 'http://localhost:8205/api/v1/reg'
        self.headers = {'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwidXNlcm5hbWUiOiJnYW5uaWN1cyIsImV4cCI6MTU1MDMyMzY3MX0.LeVaHFMM7Z3GPRtzvzQ3tUr2HTuiDnLs4AHC76voxBc'}

    def test_register_handler_post(self):
        # Testing API with the right parameters

        # Waring: If superuser in sqlite skip this testing else remove code comments
        # params = {'username': self.username1, 'email': self.email1, 'role': self.role1}
        # resp = requests.post(self.url, data=params)
        # self.assertEqual(201, resp.status_code)
        # self.assertIn('welcome', resp.text)
        # self.assertIn(self.username1, resp.text)

        # Testing API with the incorrect parameters
        # There can only be one superuser
        params2 = {'username': self.username2, 'email': self.email2, 'role': self.role1}
        resp2 = requests.post(self.url, data=params2)
        self.assertEqual(400, resp2.status_code)
        self.assertIn('superuser is exist', resp2.text)

        # Testing API with the incorrect parameters
        # User name or email is unique
        params3 = {'username': self.username1, 'email': self.email1, 'role': self.role2}
        resp3 = requests.post(self.url, data=params3)
        self.assertEqual(400, resp3.status_code)
        self.assertIn('username or email is exist', resp3.text)

        # Testing API with the incorrect parameters
        # Role can only be observers or superusers or developer
        params4 = {'username': self.username3, 'email': self.email3, 'role': self.role3}
        resp4 = requests.post(self.url, data=params4)
        self.assertEqual(400, resp4.status_code)
        self.assertIn('failed of parameters validator', resp4.text)


class LoginHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self.username = ''
        self.password = ''
        self.code = ''
        self.url = 'http://localhost:8205/api/v1/login'

    @unittest.skip('The user from sqlite. Please prepare the data before testing')
    def test_login_handler_post(self):
        # Testing API with the right parameters
        # if user role is not superuser :'code': self.code
        params = {'username': self.username, 'password': self.password}
        resp = requests.post(self.url, data=params)
        self.assertIn(self.username, resp.text)
        self.assertIn('token', resp.text)
        self.assertEqual(200, resp.status_code)

        # Testing API with the incorrect parameters
        params2 = {'username': 'Non-existent', 'password': self.password, 'code': 'flower'}
        resp2 = requests.post(self.url, data=params2)
        self.assertEqual(400, resp2.status_code)


class UserHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self.uid = 999
        self.url = 'http://localhost:8205/api/v1/user'
        self.headers = {'Authorization': ''}

    @unittest.skip('Prepare token of superuser before testing')
    def test_user_handler_get(self):
        # Testing API with the right parameters
        resp = requests.get(self.url, headers=self.headers)
        res = json.loads(resp.text)
        self.assertEqual(200, resp.status_code)
        self.assertIn("count", resp.text)
        self.assertIn("results", resp.text)
        self.assertTrue(isinstance(res, dict))
        self.assertNotEqual("successful", resp.text)
        self.assertNotEqual("failed", resp.text)

        # Testing API with the right parameters
        custom_url = self.url + '?ordering=-id'
        resp2 = requests.get(custom_url)
        self.assertEqual(200, resp2.status_code, headers=self.headers)
        self.assertIn("count", resp2.text)
        self.assertIn("results", resp2.text)
        self.assertNotEqual("successful", resp2.text)
        self.assertTrue(isinstance(json.loads(resp2.text), dict))

        # Testing API with the incorrect parameters
        custom_url2 = self.url + '?ordering=a&offset=a&wrong=a'
        resp3 = requests.get(custom_url2)
        self.assertNotEqual(200, resp3.status_code, headers=self.headers)

    def test_user_handler_put(self):
        # Testing API with the right parameters
        # The user from sqlite. Please prepare the data before testing

        # Testing API with the incorrect parameters
        params = {'id': self.uid, 'status': False}
        resp = requests.put(self.url, data=params)
        self.assertEqual(400, resp.status_code)
        self.assertIn('user dose not exist', resp.text)

    def test_user_handler_delete(self):
        # Testing API with the right parameters
        # The user from sqlite. Please prepare the data before testing

        # Testing API with the incorrect parameters
        params = {'id': self.uid}
        resp = requests.put(self.url, data=params)
        self.assertEqual(400, resp.status_code)
        self.assertIn('user dose not exist', resp.text)


if __name__ == '__main__':
    unittest.main(verbosity=2)
