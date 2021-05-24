from test_config import AppTests
from app.models import User
from app import db

class LoginTests(AppTests):

    def test_password_hashing(self):
        u = User(username='John')
        u.set_password('Abcd1234')
        self.assertFalse(u.check_password('1234Abcd'))
        self.assertTrue(u.check_password('Abcd1234'))

    def test_index_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/index', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_with_invalid_credentials(self):
        response = self.app.post('/auth/login', data=dict(username='Test', password='Test123'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)
        response = self.app.post('/auth/login', data=dict(username='Test'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This field is required', response.data)
        response = self.app.post('/auth/login', data=dict(password='Test'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This field is required', response.data)

    def test_login_logout_with_valid_credentials(self):
        u = User(username='John', email='john@example.com')
        u.set_password('john123')
        db.session.add(u)
        response = self.app.post('/auth/login', data=dict(username='John', password='john123'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hi, John!', response.data)
        self.assertIn(b'Sorry but there is nothing to display. Please create a new post.', response.data)
        response = self.app.get('/auth/logout', follow_redirects=False)
        self.assertEqual(response.status_code, 302)