from test_config import AppTests

class RegisterTests(AppTests):

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