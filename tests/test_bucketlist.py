import unittest
import os
import json
from app import create_app, db

class BucketlistTestCase(unittest.TestCase):
    """This class represents the bucketlists test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.bucketlist = {'bucket_name': 'Test one'}

        # binds the app to the current context
        with self.app.app_context():
            # creates all tables
            db.create_all()

    def test_bucket_creation(self):
        """Test POST request"""
        res = self.client().post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Test one', str(res.data))

    def test_api_can_get_all_buckets(self):
        """Test GET request"""
        res = self.client().post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/bucketlists/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Test one', str(res.data))

    def test_api_can_get_bucket_by_id(self):
        """Test GET by id"""
        rv = self.client().post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/bucketlists/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Test one', str(result.data))

    def test_bucket_can_be_edited(self):
        """Test PUT request"""
        rv = self.client().post(
            '/bucketlists/',
            data={'bucket_name': 'Test two'})
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            '/bucketlists/1',
            data={
                "bucket_name": "Test two and one"
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/bucketlists/1')
        self.assertIn('Test two and one', str(results.data))

    def test_bucket_can_be_deleted(self):
        """Test DELETE request"""
        rv = self.client().post(
            '/bucketlists/',
            data={'bucket_name': 'Test two'})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/bucketlists/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404 and a message
        result = self.client().get('/bucketlists/1')
        self.assertEqual(result.status_code, 404)
        # self.assertEqual(result.message, "Oops!Looks like that bucketlist does not exist")

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
