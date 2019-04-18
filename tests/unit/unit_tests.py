import unittest

from app import app
from app import db
from models.user_models import User
from models.user_models import TimeLine, PostComments
from models.user_models import UserRentedMovies
from models.user_models import UserRatedMovieRel
from models.user_models import UserRatedTVShowRel
from models.user_media_models import MovieComment, TVShowComment


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

    def test_signup(self):
        url = '/signup'

        # Should Return
        # 'valid_name': False,
        # 'valid_username': False,
        # 'username_taken': False,
        # 'valid_email': False,
        # 'email_taken': False,
        # 'valid_password': False,
        # 'valid_card_num': False,
        # 'success': False
        test_jsons = [{'name': None, 'username': None, 'email': None, 'password': None, 'card_num': None},
                      {'name': '',   'username': None, 'email': None, 'password': None, 'card_num': None},
                      {'name': None, 'username': '',   'email': None, 'password': None, 'card_num': None},
                      {'name': None, 'username': None, 'email': '',   'password': None, 'card_num': None},
                      {'name': None, 'username': None, 'email': None, 'password': '',   'card_num': None},
                      {'name': None, 'username': None, 'email': None, 'password': None, 'card_num': ''},
                      ]

        for test_json in test_jsons:
            result = self.app.post(url, json=test_json)
            expected = result.get_json()
            self.assertEqual(expected['valid_name'], False)
            self.assertEqual(expected['valid_username'], False)
            self.assertEqual(expected['username_taken'], False)
            self.assertEqual(expected['valid_email'], False)
            self.assertEqual(expected['email_taken'], False)
            self.assertEqual(expected['valid_password'], False)
            self.assertEqual(expected['valid_card_num'], False)
            self.assertEqual(expected['success'], False)

        # Should Be Successful Signup
        new_user = {'name': 'Unit Test',
                       'username': 'unittest',
                       'email': 'unit@test.com',
                       'password': 'pythonunittest',
                       'card_num': 123}

        result = self.app.post(url, json=new_user)
        expected = result.get_json()
        self.assertEqual(expected['name'], 'Unit Test')
        self.assertEqual(expected['username'], 'unittest')
        self.assertEqual(expected['email'], 'unit@test.com')
        self.assertEqual(expected['num_slots'], 10)
        self.assertEqual(expected['profile_pic'], "https://upload.wikimedia.org/wikipedia/en/1/13/Stick_figure.png")

        # Check if User Exists, Remove From Database if it does
        user = User.query.filter_by(name='Unit Test').filter_by(username='unittest').first()
        assert user is not None
        User.query.filter_by(name='Unit Test').filter_by(username='unittest').delete()
        db.session.commit()

    def test_user_movie_rating(self):
        url = '/user/movie/rating'

        # Should Return
        # 'valid_user': False
        # 'valid_movie': False
        # 'success': False
        test_jsons = [{'user_id': None, 'movie_id': None, 'rating': 5},
                   {'user_id': 0, 'movie_id': None, 'rating': 5},
                   {'user_id': None, 'movie_id': 0, 'rating': 5},
                   {'user_id': 0, 'movie_id': 0, 'rating': 5}
                   ]

        for test_json in test_jsons:
            result = self.app.post(url, json=test_json)
            expected = result.get_json()
            self.assertEqual(expected['valid_user'], False)
            self.assertEqual(expected['valid_movie'], False)
            self.assertEqual(expected['success'], False)

        # Should Return
        # 'valid_user': True
        # 'valid_movie': False
        # 'success': False
        test_jsons = [{'user_id': 1, 'movie_id': None, 'rating': 5},
                      {'user_id': 1, 'movie_id': 0, 'rating': 5}
                      ]

        for test_json in test_jsons:
            result = self.app.post(url, json=test_json)
            expected = result.get_json()
            self.assertEqual(expected['valid_user'], True)
            self.assertEqual(expected['valid_movie'], False)
            self.assertEqual(expected['success'], False)

        # Should Return
        # 'valid_user': False
        # 'valid_movie': True
        # 'success': False
        test_jsons = [{'user_id': None, 'movie_id': 1, 'rating': 5},
                      {'user_id': 0, 'movie_id': 1, 'rating': 5}
                      ]

        for test_json in test_jsons:
            result = self.app.post(url, json=test_json)
            expected = result.get_json()
            self.assertEqual(expected['valid_user'], False)
            self.assertEqual(expected['valid_movie'], True)
            self.assertEqual(expected['success'], False)

        # Should Return
        # 'valid_user': True
        # 'valid_movie': True
        # 'success': True
        user_id = 1
        movie_id = 1
        result = self.app.post(url, json={'user_id': user_id, 'movie_id': movie_id, 'rating': 5})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_movie'], True)
        self.assertEqual(expected['success'], True)

        # Check if Movie Rating Exists, Remove From Database if it does
        mr = UserRatedMovieRel.query.filter_by(user_id=user_id).filter_by(movie_id=movie_id).first()
        assert mr is not None
        UserRatedMovieRel.query.filter_by(user_id=user_id).filter_by(movie_id=movie_id).delete()
        db.session.flush()

    def test_user_tv_show_rating(self):
        url = '/user/tv_show/rating'
        result = self.app.post(url, json={'user_id': None,
                                          'tv_show_id': None,
                                          'rating': 5, })
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_tv_show'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': None,
                                          'tv_show_id': 0,
                                          'rating': 5, })
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_tv_show'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': 0,
                                          'tv_show_id': None,
                                          'rating': 5, })
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_tv_show'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': 0,
                                          'tv_show_id': 0,
                                          'rating': 5, })
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_tv_show'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': 1,
                                          'tv_show_id': None,
                                          'rating': 5, })
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_tv_show'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': 1,
                                          'tv_show_id': 0,
                                          'rating': 5, })
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_tv_show'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': None,
                                          'tv_show_id': 1,
                                          'rating': 5, })
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_tv_show'], True)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': 0,
                                          'tv_show_id': 1,
                                          'rating': 5, })
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_tv_show'], True)
        self.assertEqual(expected['success'], False)

        user_id = 1
        tv_show_id= 1
        result = self.app.post(url, json={'user_id': user_id,
                                          'tv_show_id': tv_show_id,
                                          'rating': 5, })
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_tv_show'], True)
        self.assertEqual(expected['success'], True)

        # Check if TV_Show Rating Exists, Remove From Database if it does
        tvr = UserRatedTVShowRel.query.filter_by(user_id=user_id).filter_by(tv_show_id=tv_show_id).first()
        assert tvr is not None
        UserRatedTVShowRel.query.filter_by(user_id=user_id).filter_by(tv_show_id=tv_show_id).delete()
        db.session.flush()

    def test_movie_commenting(self):
        url = '/movie/comment'
        result = self.app.post(url, json={'user_id': None,
                                          'movie_id': None,
                                          'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_movie'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': None,
                                          'movie_id': 0,
                                          'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_movie'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': 0,
                                          'movie_id': None,
                                          'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_movie'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': 0,
                                          'movie_id': 0,
                                          'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_movie'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': 1,
                                          'movie_id': None,
                                          'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_movie'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': 1,
                                          'movie_id': 0,
                                          'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_movie'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': None,
                                          'movie_id': 1,
                                          'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_movie'], True)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': 0,
                                          'movie_id': 1,
                                          'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_movie'], True)
        self.assertEqual(expected['success'], False)

        user_id = 1
        movie_id = 1

        result = self.app.post(url, json={'user_id': user_id,
                                          'movie_id': movie_id,
                                          'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_movie'], True)
        self.assertEqual(expected['success'], True)

        # Check if Movie Comment Exists, Remove From Database if it does
        mc = MovieComment.query.filter_by(user_id=user_id).filter_by(movie_id=movie_id).first()
        assert mc is not None
        MovieComment.query.filter_by(user_id=user_id).filter_by(movie_id=movie_id).delete()
        db.session.flush()

    def test_tv_show_commenting(self):
        url = '/tv_show/comment'
        result = self.app.post(url, json={'user_id': None,
                                          'tv_show_id': None,
                                          'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_tv_show'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': None,
                                          'tv_show_id': 0,
                                          'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_tv_show'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': 0,
                                          'tv_show_id': None,
                                          'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_tv_show'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': 0,
                                          'tv_show_id': 0,
                                          'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_tv_show'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': 1,
                                          'tv_show_id': None,
                                          'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_tv_show'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': 1,
                                          'tv_show_id': 0,
                                          'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_tv_show'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': None,
                                          'tv_show_id': 1,
                                          'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_tv_show'], True)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': 0,
                                          'tv_show_id': 1,
                                          'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_tv_show'], True)
        self.assertEqual(expected['success'], False)

        user_id = 1
        tv_show_id = 1

        result = self.app.post(url, json={'user_id': user_id,
                                          'tv_show_id': tv_show_id,
                                          'comment': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_tv_show'], True)
        self.assertEqual(expected['success'], True)

        # Check if TV_Show Comment Exists, Remove From Database if it does
        tvc = TVShowComment.query.filter_by(user_id=user_id).filter_by(tv_show_id=tv_show_id).first()
        assert tvc is not None
        TVShowComment.query.filter_by(user_id=user_id).filter_by(tv_show_id=tv_show_id).delete()
        db.session.flush()

    def test_rent_movie(self):
        url = '/rent_movie'

        result = self.app.post(url, json={'user_id': None,
                                          'movie_id': None})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_movie'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': None,
                                          'movie_id': 0})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_movie'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': 0,
                                          'movie_id': None})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_movie'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': 0,
                                          'movie_id': 0})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_movie'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': 1,
                                          'movie_id': None})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_movie'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': 1,
                                          'movie_id': 0})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_movie'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': None,
                                          'movie_id': 1})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_movie'], True)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': 0,
                                          'movie_id': 1})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_movie'], True)
        self.assertEqual(expected['success'], False)

        user_id = 1
        movie_id = 1

        result = self.app.post(url, json={'user_id': user_id,
                                          'movie_id': movie_id})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_movie'], True)
        self.assertEqual(expected['success'], True)

        # Check if Movie Rented Exists, Remove From Database if it does
        rm = UserRentedMovies.query.filter_by(user_id=user_id).filter_by(movie_id=movie_id).first()
        assert rm is not None
        UserRentedMovies.query.filter_by(user_id=user_id).filter_by(movie_id=movie_id).delete()
        db.session.flush()

    def test_timeline_posting(self):
        url = 'timeline/post'
        result = self.app.post(url, json={'user_id': None,
                                          'post_user_id': None,
                                          'post': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_friend'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': None,
                                          'post_user_id': 0,
                                          'post': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_friend'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': 0,
                                          'post_user_id': None,
                                          'post': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_friend'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': 0,
                                          'post_user_id': 0,
                                          'post': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_friend'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': 1,
                                          'post_user_id': None,
                                          'post': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_friend'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': 1,
                                          'post_user_id': 0,
                                          'post': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_friend'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': None,
                                          'post_user_id': 1,
                                          'post': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_friend'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': None,
                                          'post_user_id': 1,
                                          'post': 'Test'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_friend'], False)
        self.assertEqual(expected['success'], False)

        user_id = 1
        post_user_id = 1
        post = 'Test'

        result = self.app.post(url, json={'user_id': user_id,
                                          'post_user_id': post_user_id,
                                          'post': post})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_friend'], True)
        self.assertEqual(expected['success'], True)

        # Check if Timeline Post Exists, Remove From Database if it does
        tl = TimeLine.query.filter_by(post_id=expected['post_id']).first()
        assert tl is not None
        TimeLine.query.filter_by(post_id=expected['post_id']).delete()
        db.session.commit()

    def test_comment_on_posts(self):
        url = '/timeline/post/comment'
        result = self.app.post(url, json={'user_id': None,
                                          'post_user_id': None,
                                          'comment_user_id': None,
                                          'comment': 'Test',
                                          'post_id': None})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_friend'], False)
        self.assertEqual(expected['valid_post_id'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': 0,
                                          'post_user_id': None,
                                          'comment_user_id': None,
                                          'comment': 'Test',
                                          'post_id': None})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_friend'], False)
        self.assertEqual(expected['valid_post_id'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': None,
                                          'post_user_id': 0,
                                          'comment_user_id': None,
                                          'comment': 'Test',
                                          'post_id': None})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_friend'], False)
        self.assertEqual(expected['valid_post_id'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': None,
                                          'post_user_id': None,
                                          'comment_user_id': 0,
                                          'comment': 'Test',
                                          'post_id': None})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_friend'], False)
        self.assertEqual(expected['valid_post_id'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': 0,
                                          'post_user_id': 0,
                                          'comment_user_id': 0,
                                          'comment': 'Test',
                                          'post_id': 0})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], False)
        self.assertEqual(expected['valid_friend'], False)
        self.assertEqual(expected['valid_post_id'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': 1,
                                          'post_user_id': None,
                                          'comment_user_id': None,
                                          'comment': 'Test',
                                          'post_id': None})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_friend'], False)
        self.assertEqual(expected['valid_post_id'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': 1,
                                          'post_user_id': None,
                                          'comment_user_id': None,
                                          'comment': 'Test',
                                          'post_id': 0})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_friend'], False)
        self.assertEqual(expected['valid_post_id'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': 1,
                                          'post_user_id': 0,
                                          'comment_user_id': None,
                                          'comment': 'Test',
                                          'post_id': None})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_friend'], False)
        self.assertEqual(expected['valid_post_id'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': 1,
                                          'post_user_id': None,
                                          'comment_user_id': 0,
                                          'comment': 'Test',
                                          'post_id': None})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_friend'], False)
        self.assertEqual(expected['valid_post_id'], False)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': 1,
                                          'post_user_id': None,
                                          'comment_user_id': None,
                                          'comment': 'Test',
                                          'post_id': 1})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_friend'], False)
        self.assertEqual(expected['valid_post_id'], True)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': 1,
                                          'post_user_id': 0,
                                          'comment_user_id': None,
                                          'comment': 'Test',
                                          'post_id': 1})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_friend'], False)
        self.assertEqual(expected['valid_post_id'], True)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': 1,
                                          'post_user_id': None,
                                          'comment_user_id': 0,
                                          'comment': 'Test',
                                          'post_id': 1})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_friend'], False)
        self.assertEqual(expected['valid_post_id'], True)
        self.assertEqual(expected['success'], False)

        result = self.app.post(url, json={'user_id': 1,
                                          'post_user_id': 0,
                                          'comment_user_id': 0,
                                          'comment': 'Test',
                                          'post_id': 1})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_friend'], False)
        self.assertEqual(expected['valid_post_id'], True)
        self.assertEqual(expected['success'], False)

        user_id = 1
        post_user_id = 1
        comment_user_id = 1
        post_id = 1

        result = self.app.post(url, json={'user_id': user_id,
                                          'post_user_id': post_user_id,
                                          'comment_user_id': comment_user_id,
                                          'comment': 'Test',
                                          'post_id': post_id})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_friend'], True)
        self.assertEqual(expected['valid_post_id'], True)
        self.assertEqual(expected['success'], True)

        # Check if Post Comment  Exists, Remove From Database if it does
        pc = PostComments.query.filter_by(comment_id=expected['comment_id']).first()
        assert pc is not None
        PostComments.query.filter_by(comment_id=expected['comment_id']).delete()
        db.session.commit()

