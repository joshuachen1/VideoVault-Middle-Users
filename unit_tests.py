from app import app
import unittest
from flask import json, jsonify


class FlaskBookshelfTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def tearDown(self):
        pass

    def test_home_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_home_data(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/')

        # assert the response data
        self.assertEqual(result.data, b'Home Page')

    def test_user_movie_rating(self):
        result = self.app.post('/user/movie/rating', json={'user_id': 0,
                                                           'movie_id': 0,
                                                           'rating': 5, })
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_movie'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/user/movie/rating', json={'user_id': 1,
                                                           'movie_id': 0,
                                                           'rating': 5, })
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_movie'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/user/movie/rating', json={'user_id': 0,
                                                           'movie_id': 1,
                                                           'rating': 5, })
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_movie'], True)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/user/movie/rating', json={'user_id': 1,
                                                           'movie_id': 1,
                                                           'rating': 5, })
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_movie'], True)
        self.assertEqual(expected['success'], True)


