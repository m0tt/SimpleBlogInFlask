from test_config import AppTests
from app.models import Post, User
from app import db

class PostsTests(AppTests):

    def test_create_post_without_content_or_title_or_both(self):
        u = User(username='Test', email='test@test.com')
        u.set_password('test1234')
        db.session.add(u)
        response = self.app.post('/auth/login', data=dict(username='Test', password='test1234'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = self.app.post('/posts/create',
        data=dict(title='Test'),
        follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This field is required.', response.data)
        response = self.app.post('/posts/create',
        data=dict(body='Test'),
        follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This field is required.', response.data)
        response = self.app.post('/posts/create',
        follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This field is required.', response.data)

    def test_create_post(self):
        u = User(username='Test', email='test@test.com')
        u.set_password('test1234')
        db.session.add(u)
        response = self.app.post('/auth/login', data=dict(username='Test', password='test1234'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = self.app.post('/posts/create',
        data=dict(title='Test', body='Test'),
        follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Post was successfully created!', response.data)
