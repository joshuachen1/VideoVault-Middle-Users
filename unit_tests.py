import unittest

from app import app


class UnitTests(unittest.TestCase):

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
        result = self.app.post('/user/movie/rating', json={'user_id': None,
                                                           'movie_id': None,
                                                           'rating': 5, })
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_movie'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/user/movie/rating', json={'user_id': 0,
                                                           'movie_id': None,
                                                           'rating': 5, })
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_movie'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/user/movie/rating', json={'user_id': None,
                                                           'movie_id': 0,
                                                           'rating': 5, })
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_movie'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/user/movie/rating', json={'user_id': 0,
                                                           'movie_id': 0,
                                                           'rating': 5, })
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_movie'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/user/movie/rating', json={'user_id': 1,
                                                           'movie_id': None,
                                                           'rating': 5, })
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_movie'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/user/movie/rating', json={'user_id': 1,
                                                           'movie_id': 0,
                                                           'rating': 5, })
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_movie'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/user/movie/rating', json={'user_id': None,
                                                           'movie_id': 1,
                                                           'rating': 5, })
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_movie'], True)
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

    def test_user_tv_show_rating(self):
        result = self.app.post('/user/tv_show/rating', json={'user_id': None,
                                                             'tv_show_id': None,
                                                             'rating': 5, })
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_tv_show'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/user/tv_show/rating', json={'user_id': None,
                                                             'tv_show_id': 0,
                                                             'rating': 5, })
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_tv_show'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/user/tv_show/rating', json={'user_id': 0,
                                                             'tv_show_id': None,
                                                             'rating': 5, })
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_tv_show'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/user/tv_show/rating', json={'user_id': 0,
                                                             'tv_show_id': 0,
                                                             'rating': 5, })
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_tv_show'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/user/tv_show/rating', json={'user_id': 1,
                                                             'tv_show_id': None,
                                                             'rating': 5, })
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_tv_show'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/user/tv_show/rating', json={'user_id': 1,
                                                             'tv_show_id': 0,
                                                             'rating': 5, })
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_tv_show'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/user/tv_show/rating', json={'user_id': None,
                                                             'tv_show_id': 1,
                                                             'rating': 5, })
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_tv_show'], True)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/user/tv_show/rating', json={'user_id': 0,
                                                             'tv_show_id': 1,
                                                             'rating': 5, })
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_tv_show'], True)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/user/tv_show/rating', json={'user_id': 1,
                                                             'tv_show_id': 1,
                                                             'rating': 5, })
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_tv_show'], True)
        self.assertEqual(expected['success'], True)

    def test_movie_commenting(self):
        result = self.app.post('/movie/comment', json={'user_id': None,
                                                       'movie_id': None,
                                                       'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_movie'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/movie/comment', json={'user_id': None,
                                                       'movie_id': 0,
                                                       'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_movie'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/movie/comment', json={'user_id': 0,
                                                       'movie_id': None,
                                                       'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_movie'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/movie/comment', json={'user_id': 0,
                                                       'movie_id': 0,
                                                       'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_movie'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/movie/comment', json={'user_id': 1,
                                                       'movie_id': None,
                                                       'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_movie'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/movie/comment', json={'user_id': 1,
                                                       'movie_id': 0,
                                                       'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_movie'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/movie/comment', json={'user_id': None,
                                                       'movie_id': 1,
                                                       'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_movie'], True)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/movie/comment', json={'user_id': 0,
                                                       'movie_id': 1,
                                                       'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_movie'], True)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/movie/comment', json={'user_id': 1,
                                                       'movie_id': 1,
                                                       'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_movie'], True)
        self.assertEqual(expected['success'], True)

    def test_tv_show_commenting(self):
        result = self.app.post('/tv_show/comment', json={'user_id': None,
                                                         'tv_show_id': None,
                                                         'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_tv_show'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/tv_show/comment', json={'user_id': None,
                                                         'tv_show_id': 0,
                                                         'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_tv_show'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/tv_show/comment', json={'user_id': 0,
                                                         'tv_show_id': None,
                                                         'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_tv_show'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/tv_show/comment', json={'user_id': 0,
                                                         'tv_show_id': 0,
                                                         'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_tv_show'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/tv_show/comment', json={'user_id': 1,
                                                         'tv_show_id': None,
                                                         'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_tv_show'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/tv_show/comment', json={'user_id': 1,
                                                         'tv_show_id': 0,
                                                         'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_tv_show'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/tv_show/comment', json={'user_id': None,
                                                         'tv_show_id': 1,
                                                         'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_tv_show'], True)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/tv_show/comment', json={'user_id': 0,
                                                         'tv_show_id': 1,
                                                         'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_tv_show'], True)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/tv_show/comment', json={'user_id': 1,
                                                         'tv_show_id': 1,
                                                         'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_tv_show'], True)
        self.assertEqual(expected['success'], True)

    def test_rent_movie(self):
        result = self.app.post('/rent_movie', json={'user_id': None,
                                                    'movie_id': None})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_movie'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/rent_movie', json={'user_id': None,
                                                    'movie_id': 0})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_movie'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/rent_movie', json={'user_id': 0,
                                                    'movie_id': None})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_movie'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/rent_movie', json={'user_id': 0,
                                                    'movie_id': 0})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_movie'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/rent_movie', json={'user_id': 1,
                                                    'movie_id': None})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_movie'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/rent_movie', json={'user_id': 1,
                                                    'movie_id': 0})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_movie'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/rent_movie', json={'user_id': None,
                                                    'movie_id': 1})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_movie'], True)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/rent_movie', json={'user_id': 0,
                                                    'movie_id': 1})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_movie'], True)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/rent_movie', json={'user_id': 1,
                                                    'movie_id': 1})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_movie'], True)
        self.assertEqual(expected['success'], True)

    def test_timeline_posting(self):
        result = self.app.post('/timeline/post', json={'user_id': None,
                                                       'post_user_id': None,
                                                       'post': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_friend'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/timeline/post', json={'user_id': None,
                                                       'post_user_id': 0,
                                                       'post': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_friend'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/timeline/post', json={'user_id': 0,
                                                       'post_user_id': None,
                                                       'post': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_friend'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/timeline/post', json={'user_id': 0,
                                                       'post_user_id': 0,
                                                       'post': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_friend'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/timeline/post', json={'user_id': 1,
                                                       'post_user_id': None,
                                                       'post': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_friend'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/timeline/post', json={'user_id': 1,
                                                       'post_user_id': 0,
                                                       'post': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_friend'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/timeline/post', json={'user_id': None,
                                                       'post_user_id': 1,
                                                       'post': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_friend'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/timeline/post', json={'user_id': None,
                                                       'post_user_id': 1,
                                                       'post': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_friend'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post('/timeline/post', json={'user_id': 1,
                                                       'post_user_id': 1,
                                                       'post': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_friend'], True)
        self.assertEqual(expected['success'], True)

