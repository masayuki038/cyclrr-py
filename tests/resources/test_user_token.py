import unittest
import json

from cyclrr import create_app, db
from cyclrr.models.user import User

class UserTokenResourceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        user = User(user_name='test-login-success', password='test-login-pass', first_name='test', last_name='login', mail='test-login@test.com')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.query(User).filter(User.user_name == 'test-login-success').delete()
        db.session.commit()
        db.session.remove()
        self.app_context.pop()

    def test_login_success(self):
        js = '{"user_name": "test-login-success", "password": "test-login-pass"}'
        client = self.app.test_client()
        response = client.post('/user/token', data=js, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_login_fail_by_id(self):
        js = '{"user_name": "test-login-fail", "password": "test-login-pass"}'
        client = self.app.test_client()
        response = client.post('/user/token', data=js, content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_login_fail_by_password(self):
        js = '{"user_name": "test-login-success", "password": "test-login-pas"}'
        client = self.app.test_client()
        response = client.post('/user/token', data=js, content_type='application/json')
        self.assertEqual(response.status_code, 401)    

    def test_logout_success(self):
        self.test_login_success()

        client = self.app.test_client()
        response = client.delete('/user/token')
        self.assertEqual(response.status_code, 200)