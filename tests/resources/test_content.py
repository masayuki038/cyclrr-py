import unittest
import datetime
import json

from flask import Flask

from cyclrr import setup, db
from cyclrr.models.user import User
from cyclrr.models.content import Content

class UserResourceTestCase(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        self.app = setup(app)
        app.login_manager.init_app(app)
        self.client = self.app.test_client(app)
        self.app_context = self.app.app_context()
        self.app_context.push()
        user = User(user_name='janedoe', password='janedoe-pass', first_name='jane', last_name='doe', mail='janedoe@test.com')
        user2 = User(user_name='johndoe', password='johndoe-pass', first_name='john', last_name='doe', mail='johndoe@test.com')
        db.session.add(user)
        db.session.add(user2)
        user_id = db.session.query(User).filter_by(user_name='janedoe').first().id
        content = Content(user_id=user_id, title='test-title', content='test-content', display=True)
        db.session.add(content)
        db.session.commit()

        js = '{"user_name": "janedoe", "password": "janedoe-pass"}'
        response = self.client.post('/user/token', data=js, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        db.session.query(Content).filter_by(title='test-title').delete()
        db.session.query(Content).filter_by(title='sample').delete()
        db.session.query(Content).filter_by(title='sample-test').delete()
        db.session.query(User).filter_by(user_name='janedoe').delete()
        db.session.query(User).filter_by(user_name='johndoe').delete()
        db.session.commit()
        db.session.remove()
        self.app_context.pop()

    def test_contents_get_by_content_id(self):
        content = db.session.query(Content).filter_by(title='test-title').first()
        response = self.client.get('/content/' + str(content.id))
        self.assertEqual(response.status_code, 200)
        content_dict = json.loads(response.data)
        self.assertEqual(content_dict['title'], content.title)
        self.assertEqual(content_dict['content'], content.content)
        self.assertEqual(content_dict['created_at'], content.created_at.strftime('%Y-%m-%dT%H:%M:%S'))
        self.assertEqual(content_dict['updated_at'], content.updated_at.strftime('%Y-%m-%dT%H:%M:%S'))

    def test_contents_get_by_content_id_permission_denied(self):
        john = db.session.query(User).filter_by(user_name='johndoe').first()
        content = Content(user_id=john.id, title='sample-test', content='hogefoobar', display=True)
        db.session.add(content)
        db.session.commit()

        content = db.session.query(Content).filter_by(title='sample-test').first()
        response = self.client.get('/content/' + str(content.id))
        self.assertEqual(response.status_code, 403)

    def test_contents_get_by_user_id(self):
        user = db.session.query(User).filter_by(user_name='janedoe').first()
        content = db.session.query(Content).filter_by(user_id=user.id).first()
        response = self.client.get('/contents')
        self.assertEqual(response.status_code, 200)
        content_dict = json.loads(response.data)
        self.assertEqual(len(content_dict), 1)
        self.assertEqual(content_dict[0]['title'], content.title)
        self.assertEqual(content_dict[0]['display'], content.display)

    def test_contents_post(self):
        user = db.session.query(User).filter_by(user_name='janedoe').first()
        js = '{"user_id": %d, "title": "sample", "content": "foobarhoge", "display": true}' % user.id
        response = self.client.post('/contents', data=js, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        content = db.session.query(Content).filter_by(title='sample').first()
        content_dict = json.loads(response.data)
        self.assertEqual(content_dict['title'], content.title)
        self.assertEqual(content_dict['content'], content.content)
        self.assertEqual(content_dict['created_at'], content.created_at.strftime('%Y-%m-%dT%H:%M:%S'))
        self.assertEqual(content_dict['updated_at'], content.updated_at.strftime('%Y-%m-%dT%H:%M:%S'))

    def test_contents_post_permission_denied(self):
        john = db.session.query(User).filter_by(user_name='johndoe').first()
        js = '{"user_id": %d, "title": "sample", "content": "foobarhoge", "display": true}' % john.id
        response = self.client.post('/contents', data=js, content_type='application/json')
        self.assertEqual(response.status_code, 403)

        content = db.session.query(Content).filter_by(title='sample').first()
        self.assertEqual(content, None)

    def test_contents_put(self):
        content = db.session.query(Content).filter_by(title='test-title').first()
        js = '{"id": %d, "user_id": %d, "title": "sample-test", "content": "hogefoobar"}' % (content.id, content.user_id)
        response = self.client.put('/content/%d' % content.id, data=js, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        actual = db.session.query(Content).filter_by(id=content.id).first()
        self.assertEqual(actual.title, 'sample-test')
        self.assertEqual(actual.content, 'hogefoobar')
        
    def test_contents_put_permission_denied(self):
        john = db.session.query(User).filter_by(user_name='johndoe').first()
        content = db.session.query(Content).filter_by(title='test-title').first()
        js = '{"id": %d, "user_id": %d, "title": "sample-test", "content": "hogefoobar"}' % (content.id, john.id)
        response = self.client.put('/content/%d' % content.id, data=js, content_type='application/json')
        self.assertEqual(response.status_code, 403)

        content2 = db.session.query(Content).filter_by(title='test-title').first()
        self.assertEqual(content2.title, 'test-title')
        self.assertEqual(content2.content, 'test-content')

    def test_contents_delete(self):
        content = db.session.query(Content).filter_by(title='test-title').first()
        response = self.client.delete('/content/%d' % content.id)
        self.assertEqual(response.status_code, 200)

        actual = db.session.query(Content).all()
        self.assertEqual(len(actual), 0)

    def test_contents_delete_permission_denied(self):
        john = db.session.query(User).filter_by(user_name='johndoe').first()
        content = Content(user_id=john.id, title='sample-test', content='hogefoobar', display=True)
        db.session.add(content)
        db.session.commit()

        content = db.session.query(Content).filter_by(title='sample-test').first()
        response = self.client.delete('/content/%d' % content.id)
        self.assertEqual(response.status_code, 403)

        actual = db.session.query(Content).all()
        self.assertEqual(len(actual), 2)