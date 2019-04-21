import unittest

from cyclrr import create_app
from cyclrr import db
from cyclrr.models.user import User

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def test_add(self):
        user = User(user_name='test', password='test', first_name='test', last_name='test', mail='test')
        db.session.add(user)
        db.session.commit()