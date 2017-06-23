import unittest
from bucky import create_app


class TestViews(unittest.TestCase):
    """
    Testing authentication features
    """
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_register_and_login_successful(self):
        initial_db_size = len(self.app.database)
        self.client.post('/register',
                                    data={'username': 'Oj', 'password': 'pass'})
        self.assertTrue(len(self.app.database) == initial_db_size + 1, msg='Registered user should reflect in app database!')
        response = self.client.post('/login',
                                    data={'username': 'Oj', 'password': 'pass'})
        self.assertTrue(response.status_code == 302)

    def test_register_duplicate_unsuccessful(self):
        initial_db_size = len(self.app.database)
        self.client.post('/register',
                                    data={'username': 'Oj', 'password': 'another_pass'})
        self.assertTrue(len(self.app.database) == initial_db_size, msg='Should not add user with existing username in app!')

    def test_register_considers_caps_as_duplicate(self):
        initial_db_size = len(self.app.database)
        self.client.post('/register',
                                    data={'username': 'nocaps', 'password': 'another_pass'})
        self.assertTrue(len(self.app.database) == initial_db_size + 1, msg='Adds user successfully!')
        self.client.post('/register',
                                    data={'username': 'NOCAPS', 'password': 'another_pass'})
        self.assertTrue(len(self.app.database) == initial_db_size + 1, msg='Should consider caps as duplicate!')

    def test_logout(self):
        response = self.client.get('/logout')
        self.assertTrue(self.app.current_user is None, msg='current_user should be None')
