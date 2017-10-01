import os
import unittest
import json

from app import create_app, db

""" Defines class to test User API"""


class UserTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user_data = {'username': 'muchai', 'first_name': 'muchai', 'last-name': 'mercy',
                          'email': 'muchai@gmail.com', 'password': '1234'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_user_creation(self):
        """Test API can create a user"""
        res = self.client().post('/users/', data=self.user)
        self.assertEqual(res.status_code, 201)
        self.assertIn('muchai', str(res.data))

    def test_already_registered_user(self):
        """Test that a user cannot be registered twice."""
        res = self.client().post('/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        second_res = self.client().post('/auth/register', data=self.user_data)
        self.assertEqual(second_res.status_code, 202)
        # get the results returned in json format
        result = json.loads(second_res.data.decode())
        self.assertEqual(
            result['message'], "User already exists. Please login.")
