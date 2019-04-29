import unittest

from app import app
from app import db
from models.user_media_models import MovieComment, TVShowComment
from models.user_models import PendingFriends
from models.user_models import TimeLine, PostComments
from models.user_models import User, Friends
from models.user_models import UserRatedMovieRel
from models.user_models import UserRatedTVShowRel
from models.user_models import UserRentedMovies, UserSlots


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
        User.query.filter_by(username=expected['username']).delete()
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

        test_values = [['josh526chen@gmail.com', 'banana']]

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

    def test_resub(self):
        url = '/resub'

        # Check Exception Caught
        self.assertRaises(Exception, self.app.put(url, json={}))

        # Should Return
        # 'success': False,
        # 'valid_user': False,
        # 'valid_tv_shows': False,
        # 'valid_number_of_tv_shows': False

        test_values = [[None, None],
                       ['', None],
                       [None, ''],
                       ['', ''],
                       [None, 0],
                       [0, None],
                       ['', 0],
                       [0, ''],
                       [0, 0]
                       ]
        for i in range(len(test_values)):
            result = self.app.put(url, json={'user_id': test_values[i][0],
                                             'tv_show_id': test_values[i][1]})
            expected = result.get_json()
            self.assertEqual(expected['success'], False)
            self.assertEqual(expected['valid_user'], False)
            self.assertEqual(expected['valid_tv_shows'], False)
            self.assertEqual(expected['valid_number_of_tv_shows'], False)

        # Should Return
        # 'success': False,
        # 'valid_user': True,
        # 'valid_tv_shows': False,
        # 'valid_number_of_tv_shows': False

        test_values = [[1, None],
                       [1, ''],
                       [1, [1, 2, None]],
                       [1, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, None]],
                       [1, 0],
                       [1, 1],
                       [1, [1, 10000000000]]
                       ]
        for i in range(len(test_values)):
            result = self.app.put(url, json={'user_id': test_values[i][0],
                                             'tv_show_id': test_values[i][1]})
            expected = result.get_json()
            self.assertEqual(expected['success'], False)
            self.assertEqual(expected['valid_user'], True)
            self.assertEqual(expected['valid_tv_shows'], False)
            self.assertEqual(expected['valid_number_of_tv_shows'], False)

        # Should Return
        # 'success': False,
        # 'valid_user': True,
        # 'valid_tv_shows': False,
        # 'valid_number_of_tv_shows': True

        test_values = [[1, [1, 2, 3, 4, 5, 6, 7, 8, 9, 9]],
                       [1, [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]],
                       [1, [1, 2, 3, 4, 5, 6, 7, 8, 9, '']],
                       [1, [1, 2, 3, 4, 5, 6, 7, 8, 9, None]],
                       [1, [1, 2, 3, 4, 5, 6, 7, 8, 9, 1000000]]
                       ]
        for i in range(len(test_values)):
            result = self.app.put(url, json={'user_id': test_values[i][0],
                                             'tv_show_id': test_values[i][1]})
            expected = result.get_json()
            self.assertEqual(expected['success'], False)
            self.assertEqual(expected['valid_user'], True)
            self.assertEqual(expected['valid_tv_shows'], False)
            self.assertEqual(expected['valid_number_of_tv_shows'], True)

        # Should Return
        # 'success': False,
        # 'valid_user': True,
        # 'valid_tv_shows': True,
        # 'valid_number_of_tv_shows': False

        test_values = [[1, [1, 2, 3, 4, 5, 6]],
                       [1, []]
                       ]
        for i in range(len(test_values)):
            result = self.app.put(url, json={'user_id': test_values[i][0],
                                             'tv_show_id': test_values[i][1]})
            expected = result.get_json()
            self.assertEqual(expected['success'], False)
            self.assertEqual(expected['valid_user'], True)
            self.assertEqual(expected['valid_tv_shows'], True)
            self.assertEqual(expected['valid_number_of_tv_shows'], False)

        # Should Return
        # 'success': False,
        # 'valid_user': False,
        # 'valid_tv_shows': True,
        # 'valid_number_of_tv_shows': False

        test_values = [[0, [1, 2, 3, 4, 5, 6, 7, 8, 9]],
                       ['', [1, 2, 3, 4, 5, 6, 7, 8, 9]],
                       [None, [1, 2, 3, 4, 5, 6, 7, 8, 9]],
                       [None, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]],
                       ]
        for i in range(len(test_values)):
            result = self.app.put(url, json={'user_id': test_values[i][0],
                                             'tv_show_id': test_values[i][1]})
            expected = result.get_json()
            self.assertEqual(expected['success'], False)
            self.assertEqual(expected['valid_user'], False)
            self.assertEqual(expected['valid_tv_shows'], True)
            self.assertEqual(expected['valid_number_of_tv_shows'], False)

        # Should Return
        # 'success': True,
        # 'valid_user': True,
        # 'valid_tv_shows': True,
        # 'valid_number_of_tv_shows': True

        test_values = [[1, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]],
                       ]
        for i in range(len(test_values)):
            result = self.app.put(url, json={'user_id': test_values[i][0],
                                             'tv_show_id': test_values[i][1]})
            expected = result.get_json()
            self.assertEqual(expected['success'], True)
            self.assertEqual(expected['valid_user'], True)
            self.assertEqual(expected['valid_tv_shows'], True)
            self.assertEqual(expected['valid_number_of_tv_shows'], True)

    def test_delete_account(self):
        url = '/account/delete'

        # Check Exception Caught
        self.assertRaises(Exception, self.app.delete(url, json={}))

        # Should Return
        # 'valid_user': False
        # 'success': False

        test_values = [[None, None],
                       [None, ''],
                       ['', None],
                       ['', ''],
                       [None, 'bad password'],
                       ['', 'bad password']
                       ]

        for i in range(len(test_values)):
            result = self.app.delete(url, json={'user_id': test_values[i][0],
                                                'password': test_values[i][1]})
            expected = result.get_json()
            self.assertEqual(expected['valid_user'], False)
            self.assertEqual(expected['success'], False)

        # Should Return
        # 'valid_user': True
        # 'valid_password': False
        # 'success': False

        test_values = [[1, None],
                       [1, ''],
                       [1, 'test']
                       ]

        for i in range(len(test_values)):
            result = self.app.delete(url, json={'user_id': test_values[i][0],
                                                'password': test_values[i][1]})
            expected = result.get_json()
            self.assertEqual(expected['valid_user'], True)
            self.assertEqual(expected['valid_password'], False)
            self.assertEqual(expected['success'], False)

        # Should Return
        # 'valid_user': True
        # 'valid_password': True
        # 'success': True

        # Create New Account
        new_user = {'name': 'Unit Test',
                    'username': 'unittest',
                    'email': 'unit@test.com',
                    'password': 'pythonunittest',
                    'card_num': 123}

        result = self.app.post('/signup', json=new_user)
        expected = result.get_json()
        self.assertEqual(expected['name'], 'Unit Test')
        self.assertEqual(expected['username'], 'unittest')
        self.assertEqual(expected['email'], 'unit@test.com')
        self.assertEqual(expected['num_slots'], 10)
        self.assertEqual(expected['profile_pic'], "https://upload.wikimedia.org/wikipedia/en/1/13/Stick_figure.png")

        # Delete Account
        result = self.app.delete(url, json={'user_id': expected['id'],
                                            'password': 'pythonunittest'})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_password'], True)
        self.assertEqual(expected['success'], True)

    def test_update_profile_pic(self):
        url = '/update/profile_pic'

        # Check Exception Caught
        self.assertRaises(Exception, self.app.put(url, json={}))

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

        test_values = [None, '']

        for i in range(len(test_values)):
            url = '/user={user_id}/is_slots_full'.format(user_id=test_values[i])
            result = self.app.get(url)
            expected = result.get_json()
            self.assertEqual(expected['is_slots_full'], False)

        # Should Return
        # 'is_slots_full: False

        test_values = [5]

        for i in range(len(test_values)):
            url = '/user={user_id}/is_slots_full'.format(user_id=test_values[i])
            result = self.app.get(url)
            expected = result.get_json()
            self.assertEqual(expected['is_slots_full'], False)

        # Should Return
        # 'is_slots_full: True

        test_values = [2, 3]

        for i in range(len(test_values)):
            url = '/user={user_id}/is_slots_full'.format(user_id=test_values[i])
            result = self.app.get(url)
            expected = result.get_json()
            self.assertEqual(expected['is_slots_full'], True)

    def test_is_tv_show_in_slot(self):
        # Check Exception Caught
        self.assertRaises(Exception, self.app.get('/user=/tv_show=/is_tv_show_in_slot', json={}))

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

    def test_add_tv_show(self):
        url = 'add_tv_show'

        # Check Exception Caught
        self.assertRaises(Exception, self.app.get('/test_add_tv_show', json={}))

        # Should Return
        # 'success': False,
        # 'valid_user': False,
        # 'valid_tv_shows': False,
        # 'unique_tv_show': False

        test_values = [[None, None],
                       ['', None],
                       [None, ''],
                       ['', ''],
                       [None, 0],
                       [0, None],
                       ['', 0],
                       [0, ''],
                       [0, 0]
                       ]
        for i in range(len(test_values)):
            result = self.app.put(url, json={'user_id': test_values[i][0],
                                             'tv_show_id': test_values[i][1]})
            expected = result.get_json()
            self.assertEqual(expected['success'], False)
            self.assertEqual(expected['valid_user'], False)
            self.assertEqual(expected['valid_tv_show'], False)
            self.assertEqual(expected['unique_tv_show'], False)

        # Should Return
        # 'success': False,
        # 'valid_user': True,
        # 'valid_tv_shows': False,
        # 'unique_tv_show': False

        test_values = [[1, -1],
                       [1, None],
                       [1, 0],
                       [1, '']
                       ]
        for i in range(len(test_values)):
            result = self.app.put(url, json={'user_id': test_values[i][0],
                                             'tv_show_id': test_values[i][1]})
            expected = result.get_json()
            self.assertEqual(expected['success'], False)
            self.assertEqual(expected['valid_user'], True)
            self.assertEqual(expected['valid_tv_show'], False)
            self.assertEqual(expected['unique_tv_show'], False)

        # Should Return
        # 'success': False,
        # 'valid_user': False,
        # 'valid_tv_shows': True,
        # 'unique_tv_show': False

        test_values = [[None, 14],
                       [0, 14],
                       ['', 14],
                       [-1, 14]
                       ]
        for i in range(len(test_values)):
            result = self.app.put(url, json={'user_id': test_values[i][0],
                                             'tv_show_id': test_values[i][1]})
            expected = result.get_json()
            self.assertEqual(expected['success'], False)
            self.assertEqual(expected['valid_user'], False)
            self.assertEqual(expected['valid_tv_show'], True)
            self.assertEqual(expected['unique_tv_show'], False)

        # Should Return
        # 'success': False,
        # 'valid_user': True,
        # 'valid_tv_shows': True,
        # 'unique_tv_show': False

        test_values = [[1, 1],
                       [1, 2],
                       ]
        for i in range(len(test_values)):
            result = self.app.put(url, json={'user_id': test_values[i][0],
                                             'tv_show_id': test_values[i][1]})
            expected = result.get_json()
            self.assertEqual(expected['success'], False)
            self.assertEqual(expected['valid_user'], True)
            self.assertEqual(expected['valid_tv_show'], True)
            self.assertEqual(expected['unique_tv_show'], False)

        # Should Return
        # 'success': False,
        # 'valid_user': True,
        # 'valid_tv_shows': False,
        # 'unique_tv_show': True

        test_values = [[1, 100000],
                       ]
        for i in range(len(test_values)):
            result = self.app.put(url, json={'user_id': test_values[i][0],
                                             'tv_show_id': test_values[i][1]})
            expected = result.get_json()
            self.assertEqual(expected['success'], False)
            self.assertEqual(expected['valid_user'], True)
            self.assertEqual(expected['valid_tv_show'], False)
            self.assertEqual(expected['unique_tv_show'], True)

        # Should Return
        # 'success': True,
        # 'valid_user': True,
        # 'valid_tv_shows': True,
        # 'unique_tv_show': True

        test_values = [[1, 11],
                       ]
        for i in range(len(test_values)):
            result = self.app.put(url, json={'user_id': test_values[i][0],
                                             'tv_show_id': test_values[i][1]})
            expected = result.get_json()
            self.assertEqual(expected['success'], True)
            self.assertEqual(expected['valid_user'], True)
            self.assertEqual(expected['valid_tv_show'], True)
            self.assertEqual(expected['unique_tv_show'], True)

        UserSlots.query.filter_by(user_id=1).filter_by(tv_show_id=11).delete()
        test_entry = User.query.filter_by(id=1).first()
        test_entry.num_slots = test_entry.num_slots - 1
        db.session.commit()

    def test_subscribe(self):
        url = '/subscribe'

        # Check Exception Caught
        self.assertRaises(Exception, self.app.put(url, json={}))

        # Should Return
        # 'is_slot_exist': False
        # 'is_success': False

        test_jsons = [{'user_id': None, 'tv_show_id': None},
                      {'user_id': '', 'tv_show_id': None},
                      {'user_id': None, 'tv_show_id': ''},
                      {'user_id': '', 'tv_show_id': ''},
                      {'user_id': 1, 'tv_show_id': None},
                      {'user_id': 1, 'tv_show_id': ''},
                      {'user_id': 1, 'tv_show_id': 0},
                      ]
        for test_json in test_jsons:
            result = self.app.put(url, json=test_json)
            expected = result.get_json()
            self.assertEqual(expected['is_slot_exist'], False)
            self.assertEqual(expected['is_success'], False)

        # Should Return
        # 'is_slot_exist': True
        # 'is_success': True

        test_jsons = [{'user_id': 30, 'tv_show_id': 7},
                      {'user_id': 30, 'tv_show_id': 10},
                      {'user_id': 30, 'tv_show_id': '12'},
                      {'user_id': '30', 'tv_show_id': 9},
                      {'user_id': '30', 'tv_show_id': '3'},
                      ]
        for test_json in test_jsons:
            result = self.app.put(url, json=test_json)
            expected = result.get_json()
            self.assertEqual(expected['is_slot_exist'], True)
            self.assertEqual(expected['is_success'], True)

    def test_unsubscribe(self):
        url = '/unsubscribe'

        # Check Exception Caught
        self.assertRaises(Exception, self.app.put(url, json={}))

        # Should Return
        # 'is_slot_exist': False
        # 'is_success': False

        test_jsons = [{'user_id': None, 'tv_show_id': None},
                      {'user_id': '', 'tv_show_id': None},
                      {'user_id': None, 'tv_show_id': ''},
                      {'user_id': '', 'tv_show_id': ''},
                      {'user_id': 1, 'tv_show_id': None},
                      {'user_id': 1, 'tv_show_id': ''},
                      {'user_id': 1, 'tv_show_id': 0},
                      ]
        for test_json in test_jsons:
            result = self.app.put(url, json=test_json)
            expected = result.get_json()
            self.assertEqual(expected['is_slot_exist'], False)
            self.assertEqual(expected['is_success'], False)

        # Should Return
        # 'is_slot_exist': True
        # 'is_success': True

        test_jsons = [{'user_id': 30, 'tv_show_id': 7},
                      {'user_id': 30, 'tv_show_id': 10},
                      {'user_id': 30, 'tv_show_id': '12'},
                      {'user_id': '30', 'tv_show_id': 9},
                      {'user_id': '30', 'tv_show_id': '3'},
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
                       [1, 12],
                       [1, 13]
                       ]

        for i in range(len(test_values)):
            url = '/is_unsubscribed/user_id={user_id}/tv_show_id={tv_show_id}'.format(user_id=test_values[i][0],
                                                                                      tv_show_id=test_values[i][1])
            result = self.app.get(url)
            expected = result.get_json()
            self.assertEqual(expected['is_unsubscribed'], False)

        # Should Return
        # 'is_unsubscribed': True

        test_values = [[2, 2],
                       [3, 3]
                       ]

        for i in range(len(test_values)):
            url = '/is_unsubscribed/user_id={user_id}/tv_show_id={tv_show_id}'.format(user_id=test_values[i][0],
                                                                                      tv_show_id=test_values[i][1])
            result = self.app.get(url)
            expected = result.get_json()
            self.assertEqual(expected['is_unsubscribed'], True)

    def test_user_search(self):

        # Check Exception Caught
        self.assertRaises(Exception, self.app.get('/search/user=$@$@'))

        # Should Return
        # 'users': []

        test_values = [None, '', -10, '----', '$@$@$@$@$@$@$@$@$']

        for i in range(len(test_values)):
            url = '/search/user={user_info}'.format(user_info=test_values[i])
            result = self.app.get(url)
            expected = result.get_json()
            self.assertEqual(expected['users'], [])
            self.assertEqual(len(expected['users']), 0)

        # Should be Successful

        test_values = [[1],
                       [2],
                       ['1@1.com'],
                       ['hbo@hbo.hbo']]

        for i in range(len(test_values)):
            url = '/search/user={user_info}'.format(user_info=test_values[i][0])
            result = self.app.get(url)
            expected = result.get_json()
            assert len(expected['users']) > 0

    def test_send_friend_request(self):
        url = '/send_friend_request'

        # Check Exception Caught
        self.assertRaises(Exception, self.app.post(url, json={}))

        # Should Return
        # 'valid_user_to': False
        # 'valid_user_from': False
        # 'not_friends_already': False
        # 'success': False

        test_values = [[None, None],
                       [None, ''],
                       ['', None],
                       ['', '']
                       ]
        for i in range(len(test_values)):
            result = self.app.post(url, json={'request_to': test_values[i][0],
                                              'request_from': test_values[i][1]})
            expected = result.get_json()
            self.assertEqual(expected['valid_user_to'], False)
            self.assertEqual(expected['valid_user_from'], False)
            self.assertEqual(expected['not_already_friends'], False)
            self.assertEqual(expected['success'], False)

        # Should Return
        # 'valid_user_to': True
        # 'valid_user_from': False
        # 'not_friends_already': False
        # 'success': False

        test_values = [[1, None],
                       [1, '']
                       ]
        for i in range(len(test_values)):
            result = self.app.post(url, json={'request_to': test_values[i][0],
                                              'request_from': test_values[i][1]})
            expected = result.get_json()
            self.assertEqual(expected['valid_user_to'], True)
            self.assertEqual(expected['valid_user_from'], False)
            self.assertEqual(expected['not_already_friends'], False)
            self.assertEqual(expected['success'], False)

        # Should Return
        # 'valid_user_to': False
        # 'valid_user_from': True
        # 'not_friends_already': False
        # 'success': False

        test_values = [[None, 1],
                       ['', 1]
                       ]
        for i in range(len(test_values)):
            result = self.app.post(url, json={'request_to': test_values[i][0],
                                              'request_from': test_values[i][1]})
            expected = result.get_json()
            self.assertEqual(expected['valid_user_to'], False)
            self.assertEqual(expected['valid_user_from'], True)
            self.assertEqual(expected['not_already_friends'], False)
            self.assertEqual(expected['success'], False)

        # Should Return
        # 'valid_user_to': True
        # 'valid_user_from': True
        # 'not_friends_already': True
        # 'success': False

        test_values = [[1, 1],
                       [2, 3]
                       ]
        for i in range(len(test_values)):
            result = self.app.post(url, json={'request_to': test_values[i][0],
                                              'request_from': test_values[i][1]})
            expected = result.get_json()
            self.assertEqual(expected['valid_user_to'], True)
            self.assertEqual(expected['valid_user_from'], True)
            self.assertEqual(expected['not_already_friends'], False)
            self.assertEqual(expected['success'], False)

        # Should be Successful
        # 'valid_user_to': True
        # 'valid_user_from': True
        # 'not_friends_already': True
        # 'success': True

        test_values = [[1, 29]
                       ]
        for i in range(len(test_values)):
            result = self.app.post(url, json={'request_to': test_values[i][0],
                                              'request_from': test_values[i][1]})
            expected = result.get_json()
            self.assertEqual(expected['valid_user_to'], True)
            self.assertEqual(expected['valid_user_from'], True)
            self.assertEqual(expected['not_already_friends'], True)
            self.assertEqual(expected['success'], True)

            PendingFriends.query.filter_by(user_id=test_values[i][0]) \
                .filter_by(pending_from_id=test_values[i][1]) \
                .delete()
            db.session.commit()

    def test_accept_friend_request(self):
        url = '/accept_friend_request'

        # Check Exception Caught
        self.assertRaises(Exception, self.app.post(url, json={}))

        # Should Return
        # 'valid_user_id': False
        # 'valid_friend_id': False
        # 'valid_friendship_request': False
        # 'success': False

        test_values = [[None, None],
                       [None, ''],
                       ['', None],
                       ['', '']
                       ]
        for i in range(len(test_values)):
            result = self.app.post(url, json={'user_id': test_values[i][0],
                                              'request_from': test_values[i][1]})
            expected = result.get_json()
            self.assertEqual(expected['valid_user_id'], False)
            self.assertEqual(expected['valid_friend_id'], False)
            self.assertEqual(expected['valid_friendship_request'], False)
            self.assertEqual(expected['success'], False)

        # Should Return
        # 'valid_user_id': True
        # 'valid_friend_id': False
        # 'valid_friendship_request': False
        # 'success': False

        test_values = [[1, None],
                       [1, '']
                       ]
        for i in range(len(test_values)):
            result = self.app.post(url, json={'user_id': test_values[i][0],
                                              'request_from': test_values[i][1]})
            expected = result.get_json()
            self.assertEqual(expected['valid_user_id'], True)
            self.assertEqual(expected['valid_friend_id'], False)
            self.assertEqual(expected['valid_friendship_request'], False)
            self.assertEqual(expected['success'], False)

        # Should Return
        # 'valid_user_id': False
        # 'valid_friend_id': True
        # 'valid_friendship_request': False
        # 'success': False

        test_values = [[None, 1],
                       ['', 1]
                       ]
        for i in range(len(test_values)):
            result = self.app.post(url, json={'user_id': test_values[i][0],
                                              'request_from': test_values[i][1]})
            expected = result.get_json()
            self.assertEqual(expected['valid_user_id'], False)
            self.assertEqual(expected['valid_friend_id'], True)
            self.assertEqual(expected['valid_friendship_request'], False)
            self.assertEqual(expected['success'], False)

        # Should Return
        # 'valid_user_id': True
        # 'valid_friend_id': True
        # 'valid_friendship_request': False
        # 'success': False

        test_values = [[1, 1],
                       [2, 3]
                       ]
        for i in range(len(test_values)):
            result = self.app.post(url, json={'user_id': test_values[i][0],
                                              'request_from': test_values[i][1]})
            expected = result.get_json()
            self.assertEqual(expected['valid_user_id'], True)
            self.assertEqual(expected['valid_friend_id'], True)
            self.assertEqual(expected['valid_friendship_request'], False)
            self.assertEqual(expected['success'], False)

        # Should Return
        # 'valid_user_id': True
        # 'valid_friend_id': True
        # 'valid_friendship_request': True
        # 'success': True

        test_values = [[30, 1]]

        # Create Friend Request
        new_friend_request = PendingFriends(
            user_id=test_values[0][0],
            pending_from_id=test_values[0][1],
        )
        db.session.add(new_friend_request)
        db.session.commit()

        # Accept Friend Request
        for i in range(len(test_values)):
            result = self.app.post(url, json={'user_id': test_values[i][0],
                                              'request_from': test_values[i][1]})
            expected = result.get_json()
            self.assertEqual(expected['valid_user_id'], True)
            self.assertEqual(expected['valid_friend_id'], True)
            self.assertEqual(expected['valid_friendship_request'], True)
            self.assertEqual(expected['success'], True)

        # Remove from Friends Table
        Friends.query.filter_by(user_id=test_values[0][0]).filter_by(friend_id=test_values[0][1]).delete()
        Friends.query.filter_by(user_id=test_values[0][1]).filter_by(friend_id=test_values[0][0]).delete()
        db.session.commit()

    def test_decline_friend_request(self):
        url = '/decline_friend_request'

        # Check Exception Caught
        self.assertRaises(Exception, self.app.post(url, json={}))

        # Should Return
        # 'valid_user_id': False
        # 'valid_friend_id': False
        # 'valid_friendship_request': False
        # 'success': False

        test_values = [[None, None],
                       [None, ''],
                       ['', None],
                       ['', '']
                       ]
        for i in range(len(test_values)):
            result = self.app.post(url, json={'user_id': test_values[i][0],
                                              'request_from': test_values[i][1]})
            expected = result.get_json()
            self.assertEqual(expected['valid_user_id'], False)
            self.assertEqual(expected['valid_friend_id'], False)
            self.assertEqual(expected['valid_friendship_request'], False)
            self.assertEqual(expected['success'], False)

        # Should Return
        # 'valid_user_id': True
        # 'valid_friend_id': False
        # 'valid_friendship_request': False
        # 'success': False

        test_values = [[1, None],
                       [1, '']
                       ]
        for i in range(len(test_values)):
            result = self.app.post(url, json={'user_id': test_values[i][0],
                                              'request_from': test_values[i][1]})
            expected = result.get_json()
            self.assertEqual(expected['valid_user_id'], True)
            self.assertEqual(expected['valid_friend_id'], False)
            self.assertEqual(expected['valid_friendship_request'], False)
            self.assertEqual(expected['success'], False)

        # Should Return
        # 'valid_user_id': False
        # 'valid_friend_id': True
        # 'valid_friendship_request': False
        # 'success': False

        test_values = [[None, 1],
                       ['', 1]
                       ]
        for i in range(len(test_values)):
            result = self.app.post(url, json={'user_id': test_values[i][0],
                                              'request_from': test_values[i][1]})
            expected = result.get_json()
            self.assertEqual(expected['valid_user_id'], False)
            self.assertEqual(expected['valid_friend_id'], True)
            self.assertEqual(expected['valid_friendship_request'], False)
            self.assertEqual(expected['success'], False)

        # Should Return
        # 'valid_user_id': True
        # 'valid_friend_id': True
        # 'valid_friendship_request': False
        # 'success': False

        test_values = [[1, 1],
                       [2, 3]
                       ]
        for i in range(len(test_values)):
            result = self.app.post(url, json={'user_id': test_values[i][0],
                                              'request_from': test_values[i][1]})
            expected = result.get_json()
            self.assertEqual(expected['valid_user_id'], True)
            self.assertEqual(expected['valid_friend_id'], True)
            self.assertEqual(expected['valid_friendship_request'], False)
            self.assertEqual(expected['success'], False)

        # Should Return
        # 'valid_user_id': True
        # 'valid_friend_id': True
        # 'valid_friendship_request': True
        # 'success': True

        test_values = [[30, 1]]

        # Create Friend Request
        new_friend_request = PendingFriends(
            user_id=test_values[0][0],
            pending_from_id=test_values[0][1],
        )
        db.session.add(new_friend_request)
        db.session.commit()

        # Decline Friend Request
        for i in range(len(test_values)):
            result = self.app.post(url, json={'user_id': test_values[i][0],
                                              'request_from': test_values[i][1]})
            expected = result.get_json()
            self.assertEqual(expected['valid_user_id'], True)
            self.assertEqual(expected['valid_friend_id'], True)
            self.assertEqual(expected['valid_friendship_request'], True)
            self.assertEqual(expected['success'], True)

    def test_has_friend_request(self):

        # Should Return
        # 'has_friend_request': False

        test_values = [[None, None],
                       [None, ''],
                       ['', None],
                       ['', ''],
                       [1, None],
                       [1, ''],
                       [None, 1],
                       ['', 1],
                       [1, 1],
                       [2, 3]
                       ]
        for i in range(len(test_values)):
            result = self.app.get('/has_friend_request/user_id={}/request_from={}'.format(test_values[i][0],
                                                                                          test_values[i][1]))
            expected = result.get_json()
            self.assertEqual(expected['has_friend_request'], False)

        # Should Return
        # 'has_friend_request': True

        test_values = [[30, 1]]

        # Create Friend Request
        new_friend_request = PendingFriends(
            user_id=test_values[0][0],
            pending_from_id=test_values[0][1],
        )
        db.session.add(new_friend_request)
        db.session.commit()

        # Accept Friend Request
        for i in range(len(test_values)):
            result = self.app.get('/has_friend_request/user_id={}/request_from={}'.format(test_values[i][0],
                                                                                          test_values[i][1]))
            expected = result.get_json()
            self.assertEqual(expected['has_friend_request'], True)

        # Remove from PendingFriends Table
        PendingFriends.query.filter_by(user_id=test_values[0][0]).filter_by(pending_from_id=test_values[0][1]).delete()
        db.session.commit()

    def test_get_friend_requests(self):
        # Check Exception Caught
        self.assertRaises(Exception, self.app.get('/get_friend_requests/user=$@$@'))

        # Should Return
        # 'pending_friend_requests': []

        test_values = [None, '', -1, 0]
        for i in range(len(test_values)):
            result = self.app.get('/get_friend_requests/user={}'.format(test_values[i]))
            expected = result.get_json()
            self.assertEqual(expected['pending_friend_requests'], [])
            self.assertEqual(len(expected['pending_friend_requests']), 0)

        # Should be Successful
        result = self.app.get('/get_friend_requests/user=20')
        expected = result.get_json()
        assert len(expected['pending_friend_requests']) > 0

    def test_is_friend_request(self):
        # Check Exception Caught
        self.assertRaises(Exception, self.app.get('/is_friend_request/user=$@$@'))

        # Should Return
        # 'at_least_one_request': False

        test_values = ['', 1, None]

        for i in range(len(test_values)):
            url = '/is_friend_request/user={user_id}'.format(user_id=test_values[i])
            result = self.app.get(url)
            expected = result.get_json()
            self.assertEqual(expected['at_least_one_request'], False)

        # Should Return
        # 'at_least_one_request': False

        test_values = [20, 26, 34]

        for i in range(len(test_values)):
            url = '/is_friend_request/user={user_id}'.format(user_id=test_values[i])
            result = self.app.get(url)
            expected = result.get_json()
            self.assertEqual(expected['at_least_one_request'], True)

    def test_is_friend(self):
        # Check Exception Caught
        self.assertRaises(Exception, self.app.get('/user1=$@$@/user2='))
        self.assertRaises(Exception, self.app.get('/user1=/user2=$@$@'))
        self.assertRaises(Exception, self.app.get('/user1=$@$@/user2=$@$@'))

        # Should Return
        # 'is_friend': False

        test_values = [[None, None],
                       [None, ''],
                       ['', None],
                       ['', ''],
                       [1, None],
                       [1, ''],
                       [1, 5],
                       [5, 108]
                       ]
        for i in range(len(test_values)):
            url = '/user1={user1_id}/user2={user2_id}'.format(user1_id=test_values[i][0],
                                                              user2_id=test_values[i][1])
            result = self.app.get(url)
            expected = result.get_json()
            self.assertEqual(expected['is_friend'], False)

        # Should Return
        # 'is_friend': False

        test_values = [[1, 1],
                       [3, 5]
                       ]
        for i in range(len(test_values)):
            url = '/user1={user1_id}/user2={user2_id}'.format(user1_id=test_values[i][0],
                                                              user2_id=test_values[i][1])
            result = self.app.get(url)
            expected = result.get_json()
            self.assertEqual(expected['is_friend'], True)

    def test_get_user_friend_list(self):
        # Should Return
        # 'friends': []

        test_values = [None, '', -1, 0]

        for i in range(len(test_values)):
            url = '/user={user_id}/friends'.format(user_id=test_values[i])
            result = self.app.get(url)
            expected = result.get_json()
            self.assertEqual(expected['friends'], [])
            self.assertEqual(len(expected['friends']), 0)

        # Should Return
        # len(expected['friends']: >= 1

        test_values = [1, 2, 3]

        for i in range(len(test_values)):
            url = '/user={user_id}/friends'.format(user_id=test_values[i])
            result = self.app.get(url)
            expected = result.get_json()
            assert len(expected['friends']) >= 1

    def test_get_user_slots(self):
        # Should Return
        # 'user_slots': []

        test_values = [None, '', -1, 0]

        for i in range(len(test_values)):
            url = '/user={user_id}/slots'.format(user_id=test_values[i])
            result = self.app.get(url)
            expected = result.get_json()
            self.assertEqual(expected['user_slots'], [])
            self.assertEqual(len(expected['user_slots']), 0)

        # Should Return
        # 'user_slots': is not None

        test_values = [1, 3, 5]

        for i in range(len(test_values)):
            url = '/user={user_id}/slots'.format(user_id=test_values[i])
            result = self.app.get(url)
            expected = result.get_json()
            assert expected['user_slots'] is not None

    def test_get_user_movie_list(self):
        # Should Return
        # 'movie_list': []

        test_values = [None, '', -1, 0]

        for i in range(len(test_values)):
            url = '/user={user_id}/movie_list'.format(user_id=test_values[i])
            result = self.app.get(url)
            expected = result.get_json()
            self.assertEqual(expected['movie_list'], [])
            self.assertEqual(len(expected['movie_list']), 0)

        # Should Return
        # 'movie_list': is not None

        test_values = [1, 3, 5]

        for i in range(len(test_values)):
            url = '/user={user_id}/movie_list'.format(user_id=test_values[i])
            result = self.app.get(url)
            expected = result.get_json()
            assert expected['movie_list'] is not None

    def test_get_user_movie_rating(self):
        # Should Return
        # 'movie_rating': None

        test_values = [[None, None],
                       [None, ''],
                       ['', None],
                       ['', ''],
                       [1, None],
                       [1, ''],
                       [None, 1],
                       ['', 1],
                       ]

        for i in range(len(test_values)):
            url = '/user={user_id}/movie={movie_id}/rating'.format(user_id=test_values[i][0],
                                                                   movie_id=test_values[i][1])
            result = self.app.get(url)
            expected = result.get_json()
            assert expected['movie_rating'] is None

        # Should Return
        # 'movie_rating': is not None

        test_values = [[1, 1],
                       [1, 4]
                       ]

        for i in range(len(test_values)):
            url = '/user={user_id}/movie={movie_id}/rating'.format(user_id=test_values[i][0],
                                                                   movie_id=test_values[i][1])
            result = self.app.get(url)
            expected = result.get_json()
            assert expected['movie_rating'] is not None

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
        mr = UserRatedMovieRel.query.filter_by(user_id=user_id).filter_by(movie_id=movie_id).first()

        result = self.app.post(url, json={'user_id': user_id, 'movie_id': movie_id, 'rating': mr.user_rating})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_movie'], True)
        self.assertEqual(expected['success'], True)

        # Should Return
        # 'valid_user': True
        # 'valid_movie': True
        # 'success': True
        user_id = 30
        movie_id = 30
        result = self.app.post(url, json={'user_id': user_id, 'movie_id': movie_id, 'rating': 4})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_movie'], True)
        self.assertEqual(expected['success'], True)

        # Check if Movie Rating Exists, Remove From Database if it does
        mr = UserRatedMovieRel.query.filter_by(user_id=user_id).filter_by(movie_id=movie_id).first()
        assert mr is not None
        UserRatedMovieRel.query.filter_by(user_id=user_id).filter_by(movie_id=movie_id).delete()
        db.session.commit()

    def test_comment_movie(self):
        url = '/movie/comment'

        # Check Exception Caught
        self.assertRaises(Exception, self.app.post(url, json={}))

        test_values = [[None, None, 'Test'],
                       [None, 0, 'Test'],
                       [0, None, 'Test'],
                       [0, 0, 'Test']]
        # Check Exception Caught
        self.assertRaises(Exception, self.app.post(url, json={}))
        for i in range(len(test_values)):
            result = self.app.post(url, json={'user_id': test_values[i][0],
                                              'movie_id': test_values[i][1],
                                              'comment': test_values[i][2]})
            expected = result.get_json()
            self.assertEqual(expected['valid_user'], False)
            self.assertEqual(expected['valid_movie'], False)
            self.assertEqual(expected['success'], False)

        test_values = [[1, None, 'Test'],
                       [1, 0, 'Test']]
        # Check Exception Caught
        self.assertRaises(Exception, self.app.post(url, json={}))
        for i in range(len(test_values)):
            result = self.app.post(url, json={'user_id': test_values[i][0],
                                              'movie_id': test_values[i][1],
                                              'comment': test_values[i][2]})
            expected = result.get_json()
            self.assertEqual(expected['valid_user'], True)
            self.assertEqual(expected['valid_movie'], False)
            self.assertEqual(expected['success'], False)

        test_values = [[None, 1, 'Test'],
                       [0, 1, 'Test']]
        # Check Exception Caught
        self.assertRaises(Exception, self.app.post(url, json={}))
        for i in range(len(test_values)):
            result = self.app.post(url, json={'user_id': test_values[i][0],
                                              'movie_id': test_values[i][1],
                                              'comment': test_values[i][2]})
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

    def test_get_movie_comments(self):
        # Should return
        # 'valid_movie': False

        test_values = [None,
                       '',
                       '$@$@$@',
                       12345]
        for i in range(len(test_values)):
            url = '/movie={title}/comments'.format(title=test_values[i])
            result = self.app.get(url)
            expected = result.get_json()
            self.assertEqual(expected['valid_movie'], False)

        # Should be Successful

        test_values = ['Bird Box',
                       'Toy Story']

        for i in range(len(test_values)):
            url = '/movie={title}/comments'.format(title=test_values[i])
            result = self.app.get(url)
            expected = result.get_json()
            assert len(expected['comments']) > 0

        for i in range(len(test_values)):
            url = '/movie={title}/comments/reverse={reverse}'.format(title=test_values[i],
                                                                     reverse=True)
            result = self.app.get(url)
            expected = result.get_json()
            assert len(expected['comments']) > 0

    def test_user_tv_show_list(self):
        # Should Return
        # 'tv_show_list': []

        test_values = [None, '', -1, 0]

        for i in range(len(test_values)):
            url = '/user={user_id}/tv_show_list'.format(user_id=test_values[i])
            result = self.app.get(url)
            expected = result.get_json()
            self.assertEqual(expected['tv_show_list'], [])
            self.assertEqual(len(expected['tv_show_list']), 0)

        # Should Return
        # 'tv_show_list': is not None

        test_values = [1, 3, 5]

        for i in range(len(test_values)):
            url = '/user={user_id}/tv_show_list'.format(user_id=test_values[i])
            result = self.app.get(url)
            expected = result.get_json()
            assert expected['tv_show_list'] is not None

    def test_get_user_tv_show_rating(self):
        # Should Return
        # 'tv_show_rating': None

        test_values = [[None, None],
                       [None, ''],
                       ['', None],
                       ['', ''],
                       [1, None],
                       [1, ''],
                       [None, 1],
                       ['', 1],
                       ]

        for i in range(len(test_values)):
            url = '/user={user_id}/tv_show={tv_show_id}/rating'.format(user_id=test_values[i][0],
                                                                       tv_show_id=test_values[i][1])
            result = self.app.get(url)
            expected = result.get_json()
            assert expected['tv_show_rating'] is None

        # Should Return
        # 'tv_show_rating': is not None

        test_values = [[30, 10],
                       [30, 4]
                       ]

        for i in range(len(test_values)):
            url = '/user={user_id}/tv_show={tv_show_id}/rating'.format(user_id=test_values[i][0],
                                                                       tv_show_id=test_values[i][1])
            result = self.app.get(url)
            expected = result.get_json()
            assert expected['tv_show_rating'] is not None

    def test_rate_tv_show(self):
        url = '/user/tv_show/rating'
        # Check Exception Caught
        self.assertRaises(Exception, self.app.post(url, json={}))

        test_values = [[None, None, 5], [None, 0, 5], [0, None, 5], [0, 0, 5]]
        for i in range(len(test_values)):
            result = self.app.post(url, json={'user_id': test_values[i][0],
                                              'tv_show_id': test_values[i][1],
                                              'rating': test_values[i][2]})
            expected = result.get_json()
            self.assertEqual(expected['valid_user'], False)
            self.assertEqual(expected['valid_tv_show'], False)
            self.assertEqual(expected['success'], False)

        test_values = [[1, None, 5], [1, 0, 5]]
        for i in range(len(test_values)):
            result = self.app.post(url, json={'user_id': test_values[i][0],
                                              'tv_show_id': test_values[i][1],
                                              'rating': test_values[i][2]})
            expected = result.get_json()
            self.assertEqual(expected['valid_user'], True)
            self.assertEqual(expected['valid_tv_show'], False)
            self.assertEqual(expected['success'], False)

        test_values = [[None, 1, 5], [0, 1, 5]]
        for i in range(len(test_values)):
            result = self.app.post(url, json={'user_id': test_values[i][0],
                                              'tv_show_id': test_values[i][1],
                                              'rating': test_values[i][2]})
            expected = result.get_json()
            self.assertEqual(expected['valid_user'], False)
            self.assertEqual(expected['valid_tv_show'], True)
            self.assertEqual(expected['success'], False)

        # Should Return
        # 'valid_user': True
        # 'valid_tv_show': True
        # 'success': True
        user_id = 30
        tv_show_id = 10
        tvr = UserRatedTVShowRel.query.filter_by(user_id=user_id).filter_by(tv_show_id=tv_show_id).first()

        result = self.app.post(url, json={'user_id': user_id, 'tv_show_id': tv_show_id, 'rating': tvr.user_rating})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_tv_show'], True)
        self.assertEqual(expected['success'], True)

        # Should Return
        # 'valid_user': True
        # 'valid_tv_show': True
        # 'success': True
        user_id = 30
        tv_show_id = 12
        result = self.app.post(url, json={'user_id': user_id, 'tv_show_id': tv_show_id, 'rating': 4})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_tv_show'], True)
        self.assertEqual(expected['success'], True)

        # Check if TV_Show Rating Exists, Remove From Database if it does
        tvr = UserRatedTVShowRel.query.filter_by(user_id=user_id).filter_by(tv_show_id=tv_show_id).first()
        assert tvr is not None
        UserRatedTVShowRel.query.filter_by(user_id=user_id).filter_by(tv_show_id=tv_show_id).delete()
        db.session.commit()

    def test_comment_tv_show(self):
        url = '/tv_show/comment'

        test_values = [[None, None, 'Test'],
                       [None, 0, 'Test'],
                       [0, None, 'Test'],
                       [0, 0, 'Test']]
        # Check Exception Caught
        self.assertRaises(Exception, self.app.post(url, json={}))
        for i in range(len(test_values)):
            result = self.app.post(url, json={'user_id': test_values[i][0],
                                              'tv_show_id': test_values[i][1],
                                              'comment': test_values[i][2]})
            expected = result.get_json()
            self.assertEqual(expected['valid_user'], False)
            self.assertEqual(expected['valid_tv_show'], False)
            self.assertEqual(expected['success'], False)

        test_values = [[1, None, 'Test'],
                       [1, 0, 'Test']]
        # Check Exception Caught
        self.assertRaises(Exception, self.app.post(url, json={}))
        for i in range(len(test_values)):
            result = self.app.post(url, json={'user_id': test_values[i][0],
                                              'tv_show_id': test_values[i][1],
                                              'comment': test_values[i][2]})
            expected = result.get_json()
            self.assertEqual(expected['valid_user'], True)
            self.assertEqual(expected['valid_tv_show'], False)
            self.assertEqual(expected['success'], False)

        test_values = [[None, 1, 'Test'],
                       [0, 1, 'Test']]
        # Check Exception Caught
        self.assertRaises(Exception, self.app.post(url, json={}))
        for i in range(len(test_values)):
            result = self.app.post(url, json={'user_id': test_values[i][0],
                                              'tv_show_id': test_values[i][1],
                                              'comment': test_values[i][2]})
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

    def test_get_tv_show_comments(self):
        # Should return
        # 'valid_movie': False

        test_values = [None, '',
                       '$@$@$@',
                       12345]

        for i in range(len(test_values)):
            url = '/tv_show={title}/comments'.format(title=test_values[i])
            result = self.app.get(url)
            expected = result.get_json()
            self.assertEqual(expected['valid_tv_show'], False)

        # Should be Successful

        test_values = ['Seinfeld',
                       'Game of Thrones']

        for i in range(len(test_values)):
            url = '/tv_show={title}/comments'.format(title=test_values[i])
            result = self.app.get(url)
            expected = result.get_json()
            assert len(expected['comments']) > 0

        for i in range(len(test_values)):
            url = '/tv_show={title}/comments/reverse={reverse}'.format(title=test_values[i],
                                                                       reverse=True)
            result = self.app.get(url)
            expected = result.get_json()
            assert len(expected['comments']) > 0

    def test_is_movie_rented(self):
        # Should Return
        # 'is_movie_rented': False

        test_values = [[None, None],
                       [None, 0],
                       [None, ''],
                       ['', None],
                       ['', 0],
                       ['', ''],
                       [1, None],
                       [1, ''],
                       [1, 0],
                       [None, 1],
                       ['', 1],
                       [0, 1]
                       ]
        for i in range(len(test_values)):
            result = self.app.get('/user={user_id}/movie={movie_id}/is_movie_rented'.format(user_id=test_values[i][0],
                                                                                            movie_id=test_values[i][1]))
            expected = result.get_json()
            self.assertEqual(expected['is_movie_rented'], False)

        # Should Return
        # 'is_movie_rented': True

        # User 30 Rents Movie 10
        user_id = 30
        movie_id = 10

        result = self.app.post('/rent_movie', json={'user_id': user_id,
                                                    'movie_id': movie_id})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_movie'], True)
        self.assertEqual(expected['success'], True)

        for i in range(len(test_values)):
            result = self.app.get('/user={user_id}/movie={movie_id}/is_movie_rented'.format(user_id=user_id,
                                                                                            movie_id=movie_id))
            expected = result.get_json()
            self.assertEqual(expected['is_movie_rented'], True)

        # Remove Rented Movie From Database
        rm = UserRentedMovies.query.filter_by(user_id=user_id).filter_by(movie_id=movie_id).first()
        assert rm is not None
        UserRentedMovies.query.filter_by(user_id=user_id).filter_by(movie_id=movie_id).delete()
        db.session.commit()

    def test_get_user_rented_movies(self):
        # Should Return
        # 'user_rented_movies': []

        test_values = [None, '', -1, 0]
        for i in range(len(test_values)):
            result = self.app.get('/user={user_id}/rented_movies'.format(user_id=test_values[i]))
            expected = result.get_json()
            self.assertEqual(expected['user_rented_movies'], [])
            assert len(expected['user_rented_movies']) == 0

        # Should Return
        # len(expected['user_rented_movies'] >= 1

        # User 30 Rents Movie 10
        user_id = 30
        movie_id = 10

        result = self.app.post('/rent_movie', json={'user_id': user_id,
                                                    'movie_id': movie_id})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_movie'], True)
        self.assertEqual(expected['success'], True)

        for i in range(len(test_values)):
            result = self.app.get('/user={user_id}/rented_movies'.format(user_id=user_id))
            expected = result.get_json()
            assert len(expected['user_rented_movies']) >= 1

        # Remove Rented Movie From Database
        rm = UserRentedMovies.query.filter_by(user_id=user_id).filter_by(movie_id=movie_id).first()
        assert rm is not None
        UserRentedMovies.query.filter_by(user_id=user_id).filter_by(movie_id=movie_id).delete()
        db.session.commit()

    def test_rent_movie(self):
        url = '/rent_movie'

        # Check Exception Caught
        self.assertRaises(Exception, self.app.post(url, json={}))

        test_values = [[None, None],
                       [None, 0],
                       [0, None],
                       [0, 0]]
        for i in range(len(test_values)):
            result = self.app.post(url, json={'user_id': test_values[i][0],
                                              'movie_id': test_values[i][1]})
            expected = result.get_json()
            self.assertEqual(expected['valid_user'], False)
            self.assertEqual(expected['valid_movie'], False)
            self.assertEqual(expected['success'], False)

        test_values = [[1, None],
                       [1, 0]]
        for i in range(len(test_values)):
            result = self.app.post(url, json={'user_id': test_values[i][0],
                                              'movie_id': test_values[i][1]})
            expected = result.get_json()
            self.assertEqual(expected['valid_user'], True)
            self.assertEqual(expected['valid_movie'], False)
            self.assertEqual(expected['success'], False)

        test_values = [[None, 1],
                       [0, 1]]

        for i in range(len(test_values)):
            result = self.app.post(url, json={'user_id': test_values[i][0],
                                              'movie_id': test_values[i][1]})
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
        db.session.commit()

    def test_post_timeline(self):
        url = '/timeline/post'

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

    def test_display_wall(self):
        # Should Return
        # 'wall': []

        test_values = [None, '', -1, 0]

        for i in range(len(test_values)):
            result = self.app.get('/user={user_id}/wall'.format(user_id=test_values[i]))
            expected = result.get_json()
            self.assertEqual(expected['wall'], [])
            assert len(expected['wall']) == 0

        # Should Return
        # 'wall' with content

        # Post on Wall
        wall_id = 30
        user_id = 30
        post = 'Test'

        test_json = {'wall_id': wall_id, 'user_id': user_id, 'post': post}

        result = self.app.post('/timeline/post', json=test_json)
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_friend'], True)
        self.assertEqual(expected['success'], True)

        post_id = expected['post_id']

        # Comment on Wall
        result = self.app.post('/timeline/post/comment', json={'user_id': user_id,
                                                               'comment': 'Test',
                                                               'post_id': post_id})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_friend'], True)
        self.assertEqual(expected['valid_post_id'], True)
        self.assertEqual(expected['success'], True)

        comment_id = expected['comment_id']

        for i in range(len(test_values)):
            result = self.app.get('/user={user_id}/wall'.format(user_id=user_id))
            expected = result.get_json()
            assert len(expected['wall']) >= 1

        # Remove Post Comment From Database
        pc = PostComments.query.filter_by(comment_id=comment_id).first()
        assert pc is not None
        PostComments.query.filter_by(comment_id=comment_id).delete()
        db.session.commit()

        # Remove Wall Post from Timeline
        tl = TimeLine.query.filter_by(post_id=post_id).first()
        assert tl is not None
        TimeLine.query.filter_by(post_id=post_id).delete()
        db.session.commit()

    def test_display_wall(self):
        # Should Return
        # 'timeline': []

        test_values = [None, '', -1, 0]

        for i in range(len(test_values)):
            result = self.app.get('/user={user_id}/timeline'.format(user_id=test_values[i]))
            expected = result.get_json()
            self.assertEqual(expected['timeline'], [])
            assert len(expected['timeline']) == 0

        # Should Return
        # 'timeline' with content

        # Post on Wall
        wall_id = 30
        user_id = 30
        post = 'Test'

        test_json = {'wall_id': wall_id, 'user_id': user_id, 'post': post}

        result = self.app.post('/timeline/post', json=test_json)
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_friend'], True)
        self.assertEqual(expected['success'], True)

        post_id = expected['post_id']

        # Comment on Timeline
        result = self.app.post('/timeline/post/comment', json={'user_id': user_id,
                                                               'comment': 'Test',
                                                               'post_id': post_id})
        expected = result.get_json()
        self.assertEqual(expected['valid_user'], True)
        self.assertEqual(expected['valid_friend'], True)
        self.assertEqual(expected['valid_post_id'], True)
        self.assertEqual(expected['success'], True)

        comment_id = expected['comment_id']

        for i in range(len(test_values)):
            result = self.app.get('/user={user_id}/timeline'.format(user_id=user_id))
            expected = result.get_json()
            assert len(expected['timeline']) >= 1

        # Remove Post Comment From Database
        pc = PostComments.query.filter_by(comment_id=comment_id).first()
        assert pc is not None
        PostComments.query.filter_by(comment_id=comment_id).delete()
        db.session.commit()

        # Remove Wall Post from Timeline
        tl = TimeLine.query.filter_by(post_id=post_id).first()
        assert tl is not None
        TimeLine.query.filter_by(post_id=post_id).delete()
        db.session.commit()
