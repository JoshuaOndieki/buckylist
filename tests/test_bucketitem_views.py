import unittest
from bucky import create_app


class TestViews(unittest.TestCase):
    """
    Testing bucketlist items manipulation
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
        self.client.post('/addbucket',
                         data={'title': 'buck', 'description': 'buck buck buck'})

        # get the user
        user = None
        for a_user in self.app.database:
            if a_user.username == 'Oj':
                user = a_user
                break

        #get the bucket
        bucket = None
        for a_bucket in self.app.database[user]:
            if a_bucket.title == 'buck':
                bucket = a_bucket


    def tearDown(self):
        self.client.get('/logout') # logout user
        self.app_context.pop()

    def test_create_bucketitem(self):
        initial_db_size = len(self.app.database[user][bucket])
        self.client.post('/additem',
                        data={'name': 'item1', 'bucket': bucket })
        self.client.post('/additem',
                        data={'name': 'item2', 'bucket': bucket })
        self.client.post('/additem',
                        data={'name': 'item3', 'bucket': bucket })
        self.client.post('/additem',
                        data={'name': 'item4', 'bucket': bucket })
        self.client.post('/additem',
                        data={'name': 'item5', 'bucket': bucket })
        self.client.post('/additem',
                        data={'name': 'item6', 'bucket': bucket })
        self.client.post('/additem',
                        data={'name': 'item7', 'bucket': bucket })
        self.assertEqual(len(self.app.database[user][bucket]), initial_db_size + 7, msg='Adding should reflect in app database')

    def test_view_items(self):
        response = self.client.get('/')
        self.assertIn(b'item5', response.data, msg='Should be able to view items!')

    def test_update_item(self):
        # get items in list
        items = [item.name for item in self.app.database[user][bucket]]
        self.assertIn('item4', items, msg='Should have added items in app database!')
        initial_items = len(self.app.database[user][bucket])
        self.client.post('/updateitem',
                         data={'name': 'item6', 'new_name': 'item19'})
        self.assertNotIn('item6', items, msg='Should not have the previous item name in app database anymore!')
        self.assertIn('item19', items, msg='Should have updated item name in app database!')
        self.assertEqual(initial_items, len(self.app.database[user][bucket]), msg='Only an update should take place, not an addition!')

    def test_update_nonexisting_item(self):
        self.client.post('/updateitem',
                         data={'name': 'Strange', 'new_name': 'unstrange'})
        items = [item.name for item in self.app.database[user][bucket]]
        self.assertNotIn('unstrange', items, msg='Should not update a nonexisting item!')

    def test_delete_item(self):
        items = [item.name for item in self.app.database[user][bucket]]
        self.assertIn('item2', items)
        self.client.post('/deletebucket',
                         data={'name': 'Unique'})
        items = [item.name for item in self.app.database[user][bucket]]
        self.assertNotIn('item2', items, msg='Should delete a bucket item from app database')
