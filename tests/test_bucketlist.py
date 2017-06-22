import unittest
from bucky.models import BucketList


class TestBucketList(unittest.TestCase):

    def test_creates_bucketlist(self):
        test_bucket = BucketList("2017 bucket", "2017 description", 'Oj')
        self.assertEqual(test_bucket.title, '2017 bucket')
        self.assertEqual(test_bucket.description, '2017 description')
        self.assertEqual(test_bucket.owner, 'Oj')
