from config import Config
import unittest
from app import create_app, db
from app.models import User, Post

class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class AppTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
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
        self.assertIn(b'Sorry, there is nothing to display. Please create a new post.', response.data)
        response = self.app.get('/auth/logout', follow_redirects=False)
        self.assertEqual(response.status_code, 302)

    def test_register_with_invalid_credentials(self):
        response = self.app.post('/auth/register',
        data=dict(username='Test'),
        follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This field is required.', response.data)
        response = self.app.post('/auth/register',
        data=dict(email='test@test.org'),
        follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This field is required.', response.data)
        response = self.app.post('/auth/register',
        data=dict(password='test123'),
        follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This field is required.', response.data)
        response = self.app.post('/auth/register',
        data=dict(password2='test123'),
        follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This field is required.', response.data)
        response = self.app.post('/auth/register',
        data=dict(username='Test', email='test@', password='Abcd1234', password2='Abcd4321'),
        follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid email address.', response.data)
        response = self.app.post('/auth/register',
        data=dict(username='Test', email='test@test.org', password='Abcd1234', password2='Abcd4321'),
        follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Field must be equal to password.', response.data)

    def test_register_with_valid_credentials(self):
        response = self.app.post('/auth/register',
        data=dict(username='Test', email='test@test.org', password='Abcd1234', password2='Abcd1234'),
        follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Congratulations, you are now a registered user!', response.data)

if __name__ == '__main__':
    unittest.main(verbosity=2)