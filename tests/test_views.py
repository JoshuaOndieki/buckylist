import unittest
from bucky import views
from bucky import create_app

class TestViews(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()
    
    def test_register(self):
        response = self.client.post('/register',
        data = {'username': 'Oj', 'password': 'pass'})
        self.assertTrue(response.status_code == 302)
        self.assertTrue(self.app.database['Oj'])
    
    def test_login(self):
        response = self.client.post('/login', 
        data = {'username': 'Oj', 'password': 'pass'})
        self.assertIn(b'Oj', response.data)
        self.assertTrue(response.status_code == 302)
    
    def test_logout(self):
        response = self.client.get('/logout')
        self.assertTrue(response.status_code == 302)
        self.assertIn(b'Logged out', response.data)