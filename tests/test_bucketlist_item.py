import unittest
from bucky.models import BucketListItem

class TestBucketList(unittest.TestCase):
    def test_creates_item(self):
        test_item = BucketListItem("item x", "2017 bucket")
        self.assertEqual(test_item.name, 'item x')
        self.assertTrue(test_item.bucket == '2017 bucket')
