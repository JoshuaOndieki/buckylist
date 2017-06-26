import unittest
from bucky.models import User


class TestUser(unittest.TestCase):
    def test_creates_user(self):
        test_user = User("Oj", "pass")
        self.assertEqual(test_user.username, 'Oj')
        self.assertTrue(test_user.password)
