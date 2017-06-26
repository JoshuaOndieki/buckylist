import unittest
from bucky import create_app


class TestViews(unittest.TestCase):
    """
    Testing bucketlist manipulation
    """

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        # Register and Login Client
        self.client.post('/register',
                                    data={'username': 'Oj', 'password': 'pass'})
        self.client.post('/login',
                                    data={'username': 'Oj', 'password': 'pass'})

        # get the user
        user = None
        for a_user in self.app.database:
            if a_user.username == 'Oj':
                user = a_user
                break

    def tearDown(self):
        self.client.get('/logout') # logout user
        self.app_context.pop()

    def test_create_bucketlist(self):
        initial_db_size = len(self.app.database[user])
        self.client.post('/addbucket',
                        data={'title': 'My bucket', 'description': 'Describing my bucket'})
        self.client.post('/addbucket',
                        data={'title': 'My other bucket', 'description': 'Describing my other bucket'})
        self.client.post('/addbucket',
                         data={'title': 'UpdateMe', 'description': 'Describing update' })
        self.client.post('/addbucket',
                        data={'title': 'Unique', 'description': 'Describing unique'})
        self.client.post('/addbucket',
                         data={'title': '2017 bucket', 'description': 'Describing 2017 bucket'})
        self.client.post('/addbucket',
                         data={'title': 'safefromothers', 'description': 'Describing safefromothers'})
        self.assertEqual(len(self.app.database[user]), initial_db_size + 6, msg='Should reflect in app database')

    def test_cant_create_bucketlist_when_not_logged_in(self):
        # get all bucketlists
        initial_db_size = 0
        for a_user in self.app.database:
            initial_db_size += len(self.app.database[a_user])
        self.client.get('/logout') # logout user
        self.client.post('/addbucket',
                        data={'title': 'AnonymousBucket', 'description': 'Describing Anonymous'})
        db_size = 0
        for a_user in self.app.database:
            db_size += len(self.app.database[a_user])
        self.assertTrue(initial_db_size == db_size, msg='Should not add a bucket if user is logged out!')
        #log in user again
        self.client.post('/login',
                                    data={'username': 'Oj', 'password': 'pass'})

    def test_cant_create_duplicate_buckets(self):
        initial_db_size = len(self.app.database[user])
        self.client.post('/addbucket',
                        data={'title': 'Unique', 'description': 'Describing unique duplicate'})
        db_size = len(self.app.database[user])
        self.assertEqual(initial_db_size, db_size, msg='Should not create a duplicate bucket, consider title')

    def test_view_buckets(self):
        response = self.client.get('/')
        self.assertIn(b'My bucket', response.data, msg='Should be able to view My bucket!')
        self.assertIn(b'Describing my bucket', response.data, msg='Should be able to view My bucket description!')

    def test_cant_view_buckets_not_owned(self):
        # register and login a new user
        # logout first
        self.client.get('/logout') # logout user
        self.client.post('/register',
                                    data={'username': 'Ghost', 'password': 'appear'})
        self.client.post('/login',
                                    data={'username': 'Ghost', 'password': 'appear'})
        response = self.client.get('/')
        self.assertNotIn(b'My bucket', response.data, msg='Should not be able to view another user\'s bucket!')
        self.assertNotIn(b'Describing my bucket', response.data, msg='Should not be able to view another user\'s bucket description!')

    def test_cant_view_buckets_if_logged_out(self):
        self.client.get('/logout') # logout user
        response = self.client.get('/')
        self.assertNotIn('My bucket', response.data, msg='Should not show buckets if logged out!')
        self.client.post('/login',
                                    data={'username': 'Oj', 'password': 'pass'})

    def test_update_bucket(self):
        # get buckets in list
        buckets = [bucket.title for bucket in self.app.database[user]]
        self.assertIn('2017 bucket', buckets, msg='Should have 2017 bucket in app database!')
        self.assertNotIn('2018 bucket', buckets, msg='Should not have 2018 bucket in app database!')
        initial_buckets = len(self.app.database[user])
        self.client.post('/updatebucket',
                         data={'title': '2017 bucket', 'new_title': '2018 bucket', 'new_description': 'Describing 2018 bucket' })
        self.assertNotIn('2017 bucket', buckets, msg='Should not have 2017 bucket in app database anymore!')
        self.assertIn('2018 bucket', buckets, msg='Should have 2018 bucket in app database which replaced 2017 bucket!')
        self.assertEqual(initial_buckets, len(self.app.database[user]), msg='Only an update should take place, not an addition!')

    def test_cant_update_bucket_if_not_owner(self):
        # get buckets for Oj
        oj_buckets = [bucket.title for bucket in self.app.database[user]]
        # logout oj
        self.client.get('/logout') # logout user
        # login Ghost
        self.client.post('/login',
                                    data={'username': 'Ghost', 'password': 'appear'})
        self.client.post('/updatebucket',
                         data={'title': 'Unique', 'new_title': 'Stereotype', 'new_description': 'Describing unique stereotype' })
        oj_new_buckets = [bucket.title for bucket in self.app.database[user]]
        self.assertEqual(oj_buckets, oj_new_buckets, msg='Number of buckets should remain the same!')
        self.assertIn('Unique', oj_new_buckets, msg='Bucket still remains in buckets!')
        self.assertNotIn('Stereotype', oj_new_buckets, msg='No new bucket should be added!')
        self.client.get('/logout') # logout user
        self.client.post('/login',
                                    data={'username': 'Oj', 'password': 'pass'})

    def test_update_nonexisting_bucket(self):
        self.client.post('/updatebucket',
                         data={'title': 'Strange', 'new_title': 'unstrange', 'new_description': 'Describing strange bucket' })
        buckets = [bucket.title for bucket in self.app.database[user]]
        self.assertNotIn('unstrange', buckets, msg='Should not update a nonexisting bucket!')

    def test_update_bucket_if_logged_out(self):
        self.client.get('/logout') # logout user
        self.client.post('/updatebucket',
                         data={'title': 'UpdateMe', 'new_title': 'DontDare', 'new_description': 'Describing dont dare update me' })
        buckets = [bucket.title for bucket in self.app.database[user]]
        self.assertNotIn('DontDare', buckets, msg='Should not update buckets when logged out')
        self.client.post('/login',
                                    data={'username': 'Oj', 'password': 'pass'})

    def test_delete_bucket(self):
        buckets = [bucket.title for bucket in self.app.database[user]]
        self.assertIn('Unique', buckets)
        self.client.post('/deletebucket',
                         data={'title': 'Unique'})
        buckets = [bucket.title for buckets in self.app.database[user]]
        self.assertNotIn('Unique', buckets, msg='Should delete a bucket from app database')

    def test_cant_delete_bucket_if_not_owner(self):
        # logout from oj and login to Ghost
        self.client.get('/logout') # logout user
        self.client.post('/login',
                                    data={'username': 'Ghost', 'password': 'appear'})
        self.client.post('/deletebucket',
                         data={'title': 'safefromothers'})
        buckets = [bucket.title for bucket in self.app.database[user]]
        self.assertIn('safefromothers', buckets, msg='Should not delete existing bucket if its not the owner!')
        self.client.get('/logout') # logout user
        self.client.post('/login',
                                    data={'username': 'Oj', 'password': 'pass'})
