import unittest

from app import app
from app import db
from models.user_media_models import MovieComment, TVShowComment
from models.user_models import TimeLine, PostComments
from models.user_models import User
from models.user_models import UserRatedMovieRel
from models.user_models import UserRatedTVShowRel
from models.user_models import UserRentedMovies


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

        # Check Exception Caught
        self.assertRaises(Exception, self.app.post(url, json={}))

        name = 'Unit Test'
        username = 'unittest'
        email = 'unit@test.com'
        password = 'pythonunittest'
        card_num = 123

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
                      {'name': '', 'username': None, 'email': None, 'password': None, 'card_num': None},
                      {'name': None, 'username': '', 'email': None, 'password': None, 'card_num': None},
                      {'name': None, 'username': None, 'email': '', 'password': None, 'card_num': None},
                      {'name': None, 'username': None, 'email': None, 'password': '', 'card_num': None},
                      {'name': None, 'username': None, 'email': None, 'password': None, 'card_num': ''},
                      {'name': None, 'username': 'blah', 'email': None, 'password': None, 'card_num': ''},
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

        # Should Return
        # 'valid_name': True,
        # 'valid_username': True,
        # 'username_taken': True,
        # 'valid_email': False,
        # 'email_taken': False,
        # 'valid_password': False,
        # 'valid_card_num': False,
        # 'success': False
        test_jsons = [{'name': name, 'username': 'joshuachen1', 'email': None, 'password': None, 'card_num': None},
                      {'name': name, 'username': 'gant', 'email': None, 'password': None, 'card_num': None},
                      ]

        for test_json in test_jsons:
            result = self.app.post(url, json=test_json)
            expected = result.get_json()
            self.assertEqual(expected['valid_name'], True)
            self.assertEqual(expected['valid_username'], True)
            self.assertEqual(expected['username_taken'], True)
            self.assertEqual(expected['valid_email'], False)
            self.assertEqual(expected['email_taken'], False)
            self.assertEqual(expected['valid_password'], False)
            self.assertEqual(expected['valid_card_num'], False)
            self.assertEqual(expected['success'], False)

        # Should Return
        # 'valid_name': True,
        # 'valid_username': True,
        # 'username_taken': False,
        # 'valid_email': False,
        # 'email_taken': False,
        # 'valid_password': False,
        # 'valid_card_num': False,
        # 'success': False
        test_jsons = [{'name': name, 'username': username, 'email': 'blah', 'password': None, 'card_num': None},
                      {'name': name, 'username': username, 'email': ' ', 'password': None, 'card_num': None},
                      ]

        for test_json in test_jsons:
            result = self.app.post(url, json=test_json)
            expected = result.get_json()
            self.assertEqual(expected['valid_name'], True)
            self.assertEqual(expected['valid_username'], True)
            self.assertEqual(expected['username_taken'], False)
            self.assertEqual(expected['valid_email'], False)
            self.assertEqual(expected['email_taken'], False)
            self.assertEqual(expected['valid_password'], False)
            self.assertEqual(expected['valid_card_num'], False)
            self.assertEqual(expected['success'], False)

        # Should Return
        # 'valid_name': True,
        # 'valid_username': True,
        # 'username_taken': False,
        # 'valid_email': True,
        # 'email_taken': True,
        # 'valid_password': False,
        # 'valid_card_num': False,
        # 'success': False
        test_jsons = [
            {'name': name, 'username': username, 'email': 'joshuachen1@cpp.edu', 'password': None, 'card_num': None},
            ]

        for test_json in test_jsons:
            result = self.app.post(url, json=test_json)
            expected = result.get_json()
            self.assertEqual(expected['valid_name'], True)
            self.assertEqual(expected['valid_username'], True)
            self.assertEqual(expected['username_taken'], False)
            self.assertEqual(expected['valid_email'], True)
            self.assertEqual(expected['email_taken'], True)
            self.assertEqual(expected['valid_password'], False)
            self.assertEqual(expected['valid_card_num'], False)
            self.assertEqual(expected['success'], False)

        # Should Return
        # 'valid_name': True,
        # 'valid_username': True,
        # 'username_taken': False,
        # 'valid_email': True,
        # 'email_taken': False,
        # 'valid_password': False,
        # 'valid_card_num': False,
        # 'success': False
        test_jsons = [{'name': name, 'username': username, 'email': email, 'password': None, 'card_num': None},
                      ]

        for test_json in test_jsons:
            result = self.app.post(url, json=test_json)
            expected = result.get_json()
            self.assertEqual(expected['valid_name'], True)
            self.assertEqual(expected['valid_username'], True)
            self.assertEqual(expected['username_taken'], False)
            self.assertEqual(expected['valid_email'], True)
            self.assertEqual(expected['email_taken'], False)
            self.assertEqual(expected['valid_password'], False)
            self.assertEqual(expected['valid_card_num'], False)
            self.assertEqual(expected['success'], False)

        # Should Return
        # 'valid_name': True,
        # 'valid_username': True,
        # 'username_taken': False,
        # 'valid_email': True,
        # 'email_taken': False,
        # 'valid_password': True,
        # 'valid_card_num': False,
        # 'success': False
        test_jsons = [{'name': name, 'username': username, 'email': email, 'password': password, 'card_num': None},
                      ]

        for test_json in test_jsons:
            result = self.app.post(url, json=test_json)
            expected = result.get_json()
            self.assertEqual(expected['valid_name'], True)
            self.assertEqual(expected['valid_username'], True)
            self.assertEqual(expected['username_taken'], False)
            self.assertEqual(expected['valid_email'], True)
            self.assertEqual(expected['email_taken'], False)
            self.assertEqual(expected['valid_password'], True)
            self.assertEqual(expected['valid_card_num'], False)
            self.assertEqual(expected['success'], False)

        # Should Be Successful Signup
        new_user = {'name': 'Unit Test',
                    'username': 'unittest',
                    'email': 'unit@test.com',
                    'password': 'pythonunittest',
                    'card_num': card_num}

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

    def test_login(self):
        # Should Return
        # 'invalid_email': True
        # 'invalid_password': True
        # 'login_successful': False

        test_values = [['', '']]

        for i in range(len(test_values)):
            url = '/login/email={email}/password={password}'.format(email=test_values[i][0], password=test_values[i][1])
            result = self.app.get(url)
            expected = result.get_json()
            self.assertEqual(expected['invalid_email'], True)
            self.assertEqual(expected['invalid_password'], True)
            self.assertEqual(expected['login_successful'], False)

        # Should Return
        # 'invalid_email': True
        # 'invalid_password': False
        # 'login_successful': False

        test_values = [['', 'test']]

        for i in range(len(test_values)):
            url = '/login/email={email}/password={password}'.format(email=test_values[i][0], password=test_values[i][1])
            result = self.app.get(url)
            expected = result.get_json()
            self.assertEqual(expected['invalid_email'], True)
            self.assertEqual(expected['invalid_password'], False)
            self.assertEqual(expected['login_successful'], False)

        # Should Return
        # 'invalid_email': False
        # 'invalid_password': True
        # 'login_successful': False

        test_values = [['test@gmail.com', '']]

        for i in range(len(test_values)):
            url = '/login/email={email}/password={password}'.format(email=test_values[i][0], password=test_values[i][1])
            result = self.app.get(url)
            expected = result.get_json()
            self.assertEqual(expected['invalid_email'], False)
            self.assertEqual(expected['invalid_password'], True)
            self.assertEqual(expected['login_successful'], False)

        # Should Return
        # 'invalid_email': False
        # 'invalid_password': True
        # 'login_successful': False

        test_values = [['josh526chen@gmail.com', 'test']]

        for i in range(len(test_values)):
            url = '/login/email={email}/password={password}'.format(email=test_values[i][0], password=test_values[i][1])
            result = self.app.get(url)
            expected = result.get_json()
            self.assertEqual(expected['id'], 75)
            self.assertEqual(expected['name'], "josh")
            self.assertEqual(expected['username'], "jchen")
            self.assertEqual(expected['email'], "josh526chen@gmail.com")
            self.assertEqual(expected['num_slots'], 10)
            self.assertEqual(expected['profile_pic'], "https://upload.wikimedia.org/wikipedia/en/1/13/Stick_figure.png")

    def test_update_profile_pic(self):
        url = '/update/profile_pic'

        self.assertRaises(Exception, self.app.post(url, json={}))

        # Should Return
        # 'valid_user': False
        # 'valid_pic': False
        # 'success': False
        test_jsons = [{'user_id': None, 'profile_pic': None},
                      {'user_id': '', 'profile_pic': None},
                      {'user_id': None, 'profile_pic': ''},
                      {'user_id': '', 'profile_pic': ''}
                      ]
        for test_json in test_jsons:
            result = self.app.put(url, json=test_json)
            expected = result.get_json()
            self.assertEqual(expected['valid_user'], False)
            self.assertEqual(expected['valid_pic'], False)
            self.assertEqual(expected['success'], False)

        # Should Return
        # 'valid_user': False
        # 'valid_pic': True
        # 'success': False
        test_jsons = [{'user_id': None, 'profile_pic': 'blank.png'},
                      {'user_id': '', 'profile_pic': 'blank.png'}
                      ]
        for test_json in test_jsons:
            result = self.app.put(url, json=test_json)
            expected = result.get_json()
            self.assertEqual(expected['valid_user'], False)
            self.assertEqual(expected['valid_pic'], True)
            self.assertEqual(expected['success'], False)

        # Should Return
        # 'valid_user': True
        # 'valid_pic': False
        # 'success': False
        test_jsons = [{'user_id': 2, 'profile_pic': None},
                      {'user_id': 2, 'profile_pic': ''}
                      ]
        for test_json in test_jsons:
            result = self.app.put(url, json=test_json)
            expected = result.get_json()
            self.assertEqual(expected['valid_user'], True)
            self.assertEqual(expected['valid_pic'], False)
            self.assertEqual(expected['success'], False)

        # Should be Successful
        test_json = {'user_id': 2, 'profile_pic': 'blank.png'}
        result = self.app.put(url, json=test_json)
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_pic'], True)
        self.assertEqual(expected['success'], True)

    def test_is_slots_full(self):
        # Should Return
        # 'is_slots_full: False

        test_values = [[None],
                       ['']
                       ]

        for i in range(len(test_values)):
            url = '/user={user_id}/is_slots_full'.format(user_id=test_values[i][0])
            result = self.app.get(url)
            expected = result.get_json()
            self.assertEqual(expected['is_slots_full'], False)

        # Should Return
        # 'is_slots_full: False

        test_values = [[2], [3]]

        for i in range(len(test_values)):
            url = '/user={user_id}/is_slots_full'.format(user_id=test_values[i][0])
            result = self.app.get(url)
            expected = result.get_json()
            self.assertEqual(expected['is_slots_full'], True)

    def test_is_tv_show_in_slot(self):
        # Should Return
        # 'is_tv_show_in_slot: False

        test_values = [[None, None],
                       [None, ''],
                       ['', None],
                       ['', ''],
                       [1, 12],
                       [2, 13]
                       ]

        for i in range(len(test_values)):
            url = '/user={user_id}/tv_show={tv_show_id}/is_tv_show_in_slot'.format(user_id=test_values[i][0],
                                                                                   tv_show_id=test_values[i][1])
            result = self.app.get(url)
            expected = result.get_json()
            self.assertEqual(expected['is_tv_show_in_slot'], False)

        # Should Return
        # 'is_tv_show_in_slot: True

        test_values = [[1, 1],
                       [1, 2],
                       [2, 12],
                       [2, 14]
                       ]

        for i in range(len(test_values)):
            url = '/user={user_id}/tv_show={tv_show_id}/is_tv_show_in_slot'.format(user_id=test_values[i][0],
                                                                                   tv_show_id=test_values[i][1])
            result = self.app.get(url)
            expected = result.get_json()
            self.assertEqual(expected['is_tv_show_in_slot'], True)

    def test_subscribe(self):
        url = '/subscribe'

        # Check Exception Caught
        self.assertRaises(Exception, self.app.post(url, json={}))

        # Should Return
        # 'is_slot_exist': False
        # 'is_success': False

        test_jsons = [{'user_id': None, 'tv_show_id': None},
                      {'user_id': '', 'tv_show_id': None},
                      {'user_id': None, 'tv_show_id': ''},
                      {'user_id': '', 'tv_show_id': ''},
                      {'user_id': 1, 'tv_show_id': None},
                      {'user_id': 1, 'tv_show_id': ''},
                      ]
        for test_json in test_jsons:
            result = self.app.put(url, json=test_json)
            expected = result.get_json()
            self.assertEqual(expected['is_slot_exist'], False)
            self.assertEqual(expected['is_success'], False)

        # Should Return
        # 'is_slot_exist': True
        # 'is_success': True

        test_jsons = [{'user_id': 1, 'tv_show_id': 11},
                      {'user_id': 1, 'tv_show_id': 12},
                      ]
        for test_json in test_jsons:
            result = self.app.put(url, json=test_json)
            expected = result.get_json()
            self.assertEqual(expected['is_slot_exist'], True)
            self.assertEqual(expected['is_success'], True)

    def test_is_unsubscribe(self):
        # Should Return
        # 'is_unsubscribed': False

        test_values = [[None, None],
                       [None, ''],
                       ['', None],
                       ['', ''],
                       [1, 1,
                       [1, 2]
                       ]

        for i in range(len(test_values)):
            url = '/is_unsubscribed/user_id={user_id}/tv_show_id={tv_show_id}'.format(user_id=test_values[i][0],
                                                                                      tv_show_id=test_values[i][1])
            result = self.app.get(url)
            expected = result.get_json()
            self.assertEqual(expected['is_slots_full'], False)


    def test_rate_movie(self):
        url = '/user/movie/rating'

        # Check Exception Caught
        self.assertRaises(Exception, self.app.post(url, json={}))

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

    def test_rate_tv_show(self):
        url = '/user/tv_show/rating'

        # Check Exception Caught
        self.assertRaises(Exception, self.app.post(url, json={}))

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
        tv_show_id = 1
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

    def test_comment_movie(self):
        url = '/movie/comment'

        # Check Exception Caught
        self.assertRaises(Exception, self.app.post(url, json={}))

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

        # Check Exception Caught
        self.assertRaises(Exception, self.app.post(url, json={}))

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

        # Check Exception Caught
        self.assertRaises(Exception, self.app.post(url, json={}))

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

    def test_post_timeline(self):
        url = 'timeline/post'

        # Check Exception Caught
        self.assertRaises(Exception, self.app.post(url, json={}))

        # Should Return
        # 'valid_user': False,
        # 'valid_friend': False,
        # 'success': False
        test_jsons = [{'wall_id': None, 'user_id': None, 'post': None},
                      {'wall_id': None, 'user_id': '', 'post': None},
                      {'wall_id': '', 'user_id': None, 'post': None},
                      {'wall_id': '', 'user_id': '', 'post': None},
                      ]

        for test_json in test_jsons:
            result = self.app.post(url, json=test_json)
            expected = result.get_json()
            self.assertEqual(expected['valid_user'], False)
            self.assertEqual(expected['valid_friend'], False)
            self.assertEqual(expected['success'], False)

        # Should Return
        # 'valid_user': True,
        # 'valid_friend': False,
        # 'success': False
        test_jsons = [{'wall_id': 1, 'user_id': 4, 'post': None},
                      {'wall_id': 1, 'user_id': 5, 'post': None},
                      ]

        for test_json in test_jsons:
            result = self.app.post(url, json=test_json)
            expected = result.get_json()
            self.assertEqual(expected['valid_user'], True)
            self.assertEqual(expected['valid_friend'], False)
            self.assertEqual(expected['success'], False)

        # Should be successful
        wall_id = 1
        user_id = 1
        post = 'Test'

        test_json = {'wall_id': wall_id, 'user_id': user_id, 'post': post}

        result = self.app.post(url, json=test_json)
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_friend'], True)
        self.assertEqual(expected['success'], True)

        # Check if Timeline Post Exists, Remove From Database if it does
        tl = TimeLine.query.filter_by(post_id=expected['post_id']).first()
        assert tl is not None
        TimeLine.query.filter_by(post_id=expected['post_id']).delete()
        db.session.commit()

    def test_comment_on_post(self):
        url = '/timeline/post/comment'

        # Check Exception Caught
        self.assertRaises(Exception, self.app.post(url, json={}))

        # Should Return
        # 'valid_user': False,
        # 'valid_friend': False,
        # 'valid_post_id': False,
        # 'success': False
        test_jsons = [{'post_id': None, 'user_id': None, 'comment': None},
                      {'post_id': None, 'user_id': '', 'comment': None},
                      {'post_id': '', 'user_id': None, 'comment': None},
                      {'post_id': '', 'user_id': '', 'comment': None},
                      ]

        for test_json in test_jsons:
            result = self.app.post(url, json=test_json)
            expected = result.get_json()
            self.assertEqual(expected['valid_user'], False)
            self.assertEqual(expected['valid_friend'], False)
            self.assertEqual(expected['valid_post_id'], False)
            self.assertEqual(expected['success'], False)

        # Should Return
        # 'valid_user': True,
        # 'valid_friend': False,
        # 'valid_post_id': False,
        # 'success': False
        test_jsons = [{'post_id': None, 'user_id': 1, 'comment': None},
                      {'post_id': '', 'user_id': 1, 'comment': None},
                      ]

        for test_json in test_jsons:
            result = self.app.post(url, json=test_json)
            expected = result.get_json()
            self.assertEqual(expected['valid_user'], True)
            self.assertEqual(expected['valid_friend'], False)
            self.assertEqual(expected['valid_post_id'], False)
            self.assertEqual(expected['success'], False)

        # Should Return
        # 'valid_user': True,
        # 'valid_friend': False,
        # 'valid_post_id': True,
        # 'success': False
        test_jsons = [{'post_id': 1, 'user_id': 75, 'comment': None},
                      {'post_id': 2, 'user_id': 75, 'comment': None},
                      ]

        for test_json in test_jsons:
            result = self.app.post(url, json=test_json)
            expected = result.get_json()
            self.assertEqual(expected['valid_user'], True)
            self.assertEqual(expected['valid_friend'], False)
            self.assertEqual(expected['valid_post_id'], True)
            self.assertEqual(expected['success'], False)

        post_id = 1
        user_id = 1

        result = self.app.post(url, json={'user_id': user_id,
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
