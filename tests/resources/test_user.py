import unittest
import json

from flask import Flask

from cyclrr import setup, db
from cyclrr.models.user import User

class UserResourceTestCase(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        self.app = setup(app)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def test_users_get(self):
        user = User(user_name='janedoe', password='janedoe-pass', first_name='jane', last_name='doe', mail='janedoe@test.com')
        db.session.add(user)
        db.session.commit()
        client = self.app.test_client()
        response = client.get('/users/' + str(user.id))
        self.assertEqual(response.status_code, 200)
        user_dict = json.loads(response.data)
        self.assertEqual(user_dict['user_name'], 'janedoe')
        self.assertEqual(user_dict['password'], 'janedoe-pass')
        self.assertEqual(user_dict['first_name'], 'jane')
        self.assertEqual(user_dict['last_name'], 'doe')
        self.assertEqual(user_dict['mail'], 'janedoe@test.com')

    def test_users_post(self):
        client = self.app.test_client()
        js = '{"user_name": "allanpoe", "password": "hoge", "first_name": "allan", "last_name": "poe", "mail": "allanpoe@test.com"}'
        response = client.post('/users', data=js, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        actual = json.loads(response.data)
        expected = json.loads(client.get('/users/' + str(actual['id'])).data)

        self.assertEqual(actual['user_name'], expected['user_name'])
        self.assertEqual(actual['password'], expected['password'])
        self.assertEqual(actual['first_name'], expected['first_name'])
        self.assertEqual(actual['last_name'], expected['last_name'])
        self.assertEqual(actual['mail'], expected['mail'])
        
        