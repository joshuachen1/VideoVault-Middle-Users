import math
import os
import re
from datetime import date, datetime, timedelta

import pymysql
from cryptography.fernet import Fernet
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# Setup App
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])  # Should change based on is in Development or Production
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS
CORS(app)

# Start Database
db = SQLAlchemy(app)

# Force pymysql to be used as replacement for MySQLdb
pymysql.install_as_MySQLdb()

# Enable Variable Port for Heroku
port = int(os.environ.get('PORT', 33507))

# Import Models
from Email import Email
from crypto_models import Key
from user_models import Signup, Login
from user_models import User, Friends, PendingFriends, TimeLine, Post, PostComments, PostComment
from user_models import Slot, UserSlots, DisplayUserSlots, UserRentedMovies
from user_models import UserRatedMovieRel, DisplayRatedMovie, RatedMovie
from user_models import UserRatedTVShowRel, DisplayRatedTVShow, RatedTVShow
from user_media_models import Movie, MovieComment, TVShows, TVShowComment, Comment


# Set Up Email Server
email_sender = Email(app.config['COMPANY_EMAIL'])


# [url]/
@app.route('/')
def hello_world():
    return 'Home Page'


# [url]/login/email=[email]/password=[password]
@app.route('/login/email=<email>/password=<attempted_pwd>', methods=['GET'])
@app.route('/login/email=<email>/password=', methods=['GET'])
@app.route('/login/email=/password=<attempted_pwd>', methods=['GET'])
@app.route('/login/email=/password=', methods=['GET'])
def login(email=None, attempted_pwd=None):
    try:
        user_info = User.query.filter_by(email=email).first()

        if email is None or user_info is None:
            result = Login(True, False, False)
            return jsonify(result.serialize())

        # Get Key
        key = Key.query.filter_by(id=1).first().key
        key = key.encode('utf-8')
        cipher = Fernet(key)

        # Get Decrypted User Password
        saved_pwd = user_info.password
        saved_pwd = saved_pwd.encode('utf-8')
        decrypted_saved_pwd = cipher.decrypt(saved_pwd)
        decrypted_saved_pwd = decrypted_saved_pwd.decode('utf-8')

        if decrypted_saved_pwd == attempted_pwd:
            delete_expired_movies()
            delete_expired_tv_shows()
            return jsonify(user_info.serialize())
        else:
            result = Login(False, True, False)
            return jsonify(result.serialize())
    except Exception as e:
        return str(e)


# { name: [name], username: [username], email:[email], password: [password], card_num: [card_num] }
# adds user to user table and creates 10 slots in user_slots
@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        name = str(data['name'])
        username = str(data['username'])
        email = str(data['email'])
        password = str(data['password'])
        card_num = str(data['card_num'])
        num_slots = 10
        sub_date = str(date.today())
        profile_pic = "https://upload.wikimedia.org/wikipedia/en/1/13/Stick_figure.png"

        # Check if @ sign and period after @ sign
        email_pattern = re.compile("[^@]+@[^@]+\.[^@]+")
        if email_pattern.match(email) is None:
            return jsonify({'valid_email': False})

        # Check if email exists
        check_unique = User.query.filter_by(email=email).first()
        if check_unique is not None:
            result = Signup(True, False, False)
            return jsonify(result.serialize())

        # Check if username exists
        check_unique = User.query.filter_by(username=username).first()
        if check_unique is not None:
            result = Signup(False, True, False)
            return jsonify(result.serialize())

        # Get Key
        key = Key.query.filter_by(id=1).first().key
        key = key.encode('utf-8')
        cipher = Fernet(key)

        # Encrypt User Password
        password = password.encode('utf-8')
        encrypted_pwd = cipher.encrypt(password)

        # Encrypt User Credit Card Number
        card_num = card_num.encode('utf-8')
        encrypted_cn = cipher.encrypt(card_num)

        try:
            user = User(
                name=name,
                username=username,
                email=email,
                password=encrypted_pwd,
                card_num=encrypted_cn,
                num_slots=num_slots,
                sub_date=sub_date,
                profile_pic=profile_pic,
            )
            db.session.add(user)
            email_sender.welcome_email(username=username, user_email=email)

            new_user = User.query.filter_by(username=username).first()
            for i in range(num_slots):
                slot = UserSlots(
                    user_id=new_user.id,
                    slot_num=(i + 1),
                    tv_show_id=None,
                )
                db.session.add(slot)

            # Add self to friend_list
            friend = Friends(
                user_id=new_user.id,
                friend_id=new_user.id,
            )
            db.session.add(friend)
            db.session.commit()
            return jsonify(new_user.serialize())
        except Exception as e:
            return str(e)
    except Exception as e:
        return str(e)


# { user_id: [user_id], tv_show_id: [tv_show_id_list] }
# adds 10 tv shows into user_slots table
@app.route('/resub', methods=['PUT'])
def resub():
    data = request.get_json()
    user_id = data['user_id']
    tv_show_id = data['tv_show_id']

    user_check = User.query.filter_by(id=user_id).first()
    tv_show_len = len(set(tv_show_id))

    # creating booleans
    is_success = True
    is_valid_user = True
    is_valid_tv_show = True
    is_valid_number_of_tv_shows = True
    is_slots_exist = True

    # return boolean for invalid inputs
    if tv_show_len is not 10:
        is_success = False
        is_valid_number_of_tv_shows = False
    if user_check is None:
        is_success = False
        is_valid_user = False
    if is_success is False:
        return jsonify({'success': is_success,
                        'valid_user': is_valid_user,
                        'valid_tv_shows': is_valid_tv_show,
                        'valid_number_of_tv_shows': is_valid_number_of_tv_shows,
                        'slots_exists': is_slots_exist})
    # add each entry to the user_slots table
    i = 1
    for tv_show_id in tv_show_id:
        tv_show_check = TVShows.query.filter_by(id=tv_show_id).first()

        # return boolean for invalid inputs
        if tv_show_check is None:
            is_success = False
            is_valid_tv_show = False

        slot_num = i
        is_slots_exist = add_tv_show(True, slot_num, tv_show_id, user_id)
        if is_slots_exist is False:
            is_success = False
        i = i + 1
        if is_success is False:
            return jsonify({'success': is_success,
                            'valid_user': is_valid_user,
                            'valid_tv_shows': is_valid_tv_show,
                            'valid_number_of_tv_shows': is_valid_number_of_tv_shows,
                            'slots_exists': is_slots_exist})

    db.session.commit()
    return jsonify({'success': is_success,
                    'valid_user': is_valid_user,
                    'valid_tv_shows': is_valid_tv_show,
                    'valid_number_of_tv_shows': is_valid_number_of_tv_shows,
                    'slots_exists': is_slots_exist})


# Need User Id and Password
@app.route('/account/delete', methods=['DELETE'])
def delete_account():
    try:
        data = request.get_json()
        user_id = data['user_id']
        password = data['password']

        user = User.query.filter_by(id=user_id).first()

        # Get Key
        key = Key.query.filter_by(id=1).first().key
        key = key.encode('utf-8')
        cipher = Fernet(key)

        # Check Matching Password
        true_pwd = user.password.encode('utf-8')
        decrypted_pwd = (cipher.decrypt(true_pwd)).decode('utf-8')

        if user.id is not user_id:
            return jsonify({'success:': False,
                            'valid_user': False})
        elif decrypted_pwd != password:
            return jsonify({'success:': False,
                            'valid_user': True,
                            'valid_password': False})
        else:
            # Delete From Friends Table
            Friends.query.filter_by(user_id=user_id).delete()
            Friends.query.filter_by(friend_id=user_id).delete()

            # Delete All User Comments
            MovieComment.query.filter_by(user_id=user_id).delete()
            TVShowComment.query.filter_by(user_id=user_id).delete()

            # Delete User Rated Media Lists
            movie_list = UserRatedMovieRel.query.filter_by(user_id=user_id).delete()
            for m in movie_list:
                UserRatedMovieRel.query.filter_by(movie_id=m.movie_id).delete()
                update_average_rating(False, m.movie_id)

            tv_show_list = UserRatedTVShowRel.query.filter_by(user_id=user_id).delete()
            for tvs in tv_show_list:
                UserRatedTVShowRel.query.filter_by(tv_show_id=tvs.tv_show_id).delete()
                update_average_rating(True, tvs.tv_show_id)

            # Remove All User Slots
            UserSlots.query.filter_by(user_id=user_id).delete()

            # Remove From User Table
            User.query.filter_by(id=user_id).delete()

            db.session.commit()

            return jsonify({'success:': True,
                            'valid_user': True,
                            'valid_password': True})

    except Exception as e:
        return str(e)


# { "user_id": [user_id], "profile_pic": [profile_pic] }
# [url]/update/profile_pic
@app.route('/update/profile_pic', methods=['PUT'])
def update_profile_pic():
    try:
        data = request.get_json()
        user_id = data['user_id']
        profile_pic = data['profile_pic']

        # Must end in png
        profile_pic_pattern = re.compile("[^@]+\.png")
        user = User.query.filter_by(id=user_id).first()

        if user is None and profile_pic_pattern.match(profile_pic) is None:
            return jsonify({'success': False,
                            'valid_user': False,
                            'valid_pic': False})
        elif user is None:
            return jsonify({'success': False,
                            'valid_user': False,
                            'valid_pic': True})
        elif profile_pic_pattern.match(profile_pic) is None:
            return jsonify({'success': False,
                            'valid_user': True,
                            'valid_pic': False})
        else:
            user.profile_pic = profile_pic
            db.session.commit()
            return jsonify({'success': True,
                            'valid_user': True,
                            'valid_pic': True})
    except Exception as e:
        return str(e)


# [url]/user=[user_id]/is_slots_full
@app.route('/user=<user_id>/is_slots_full', methods=['GET'])
@app.route('/user=/is_slots_full', methods=['GET'])
def is_slots_full(user_id=None):
    # Gets list of user slots to get length
    user_slots = UserSlots.query.filter_by(user_id=user_id).all()
    # Gets list of tv show ids to check for null entries later
    tv_shows_list = list()
    for slot in user_slots:
        tv_shows_list.append(slot.tv_show_id)
    user = User.query.filter_by(id=user_id).first()
    user_num_slots = user.num_slots

    # Compares length of user_slots to User's num_slots and ensures there is no null entry
    if len(user_slots) is not user_num_slots or any(tv_show is None for tv_show in tv_shows_list):
        return jsonify({'is_slots_full': False})
    else:
        return jsonify({'is_slots_full': True})


# [url]/user=[user_id]/tv_show[tv_show_id]/is_tv_show_in_slot
@app.route('/user=<user_id>/tv_show=<tv_show_id>/is_tv_show_in_slot', methods=['GET'])
@app.route('/user=/tv_show=/is_tv_show_in_slot', methods=['GET'])
def is_tv_show_in_slot(user_id=None, tv_show_id=None):
    try:
        if UserSlots.query.filter_by(user_id=user_id).filter_by(tv_show_id=tv_show_id).first() is not None:
            return jsonify({'is_tv_show_in_slot': True})
        else:
            return jsonify({'is_tv_show_in_slot': False})
    except Exception as e:
        return str(e)


# { user_id: [user_id], tv_show_id: [tv_show_id] }
# creates a new slot in user_slots and adds tv show to that slot
@app.route('/add_tv_show', methods=['PUT'])
def add_tv_show(resub=False, new_slot_id=None, tv_show_id=None, user_id=None):
    # only run this section of code to add tv show to newly added slot
    if resub is False:
        data = request.get_json()
        user_id = data['user_id']
        tv_show_id = data['tv_show_id']

        # Update user's slot number
        new_slot_id = increment_slot(user_id)

        user_check = User.query.filter_by(id=user_id).first()
        current_user_slots = UserSlots.query.filter_by(user_id=user_id).all()
        tv_show_check = TVShows.query.filter_by(id=tv_show_id).first()

        # all current tv show ids in user slots
        curr_tv_show_slot_ids = list()
        for slot in current_user_slots:
            curr_tv_show_slot_ids.append(slot.tv_show_id)

        # default boolean variables to success
        is_success = True
        is_valid_user = True
        is_valid_tv_show = True
        is_unique_tv_show = True

        # checks to see if input is valid
        if user_check is None:
            is_success = False
            is_valid_user = False
        if tv_show_check is None:
            is_success = False
            is_valid_tv_show = False
        if tv_show_id in curr_tv_show_slot_ids:
            is_success = False
            is_unique_tv_show = False
        if is_success is False:
            return jsonify({'success': is_success,
                            'valid_user': is_valid_user,
                            'valid_tv_show': is_valid_tv_show,
                            'unique_tv_show': is_unique_tv_show})

    try:
        if resub is False:
            slot = UserSlots(
                user_id=user_id,
                slot_num=new_slot_id,
                tv_show_id=tv_show_id,
            )
            db.session.add(slot)
            db.session.commit()
        else:
            data = request.get_json()
            user_slots = UserSlots.query.filter_by(user_id=user_id).filter_by(slot_num=new_slot_id).first()
            if resub is True and user_slots is None:
                return False
            user_slots.user_id = user_id,
            user_slots.slot_num = new_slot_id,
            user_slots.tv_show_id = tv_show_id,
            if resub is True and user_slots is not None:
                return True

        return jsonify({'success': True,
                        'valid_user': True,
                        'valid_tv_show': True,
                        'unique_tv_show': True, })
    except Exception as e:
        return str(e)


# { user_id: [user_id], tv_show_id: [tv_show_id] }
# boolean to convert unsubscribe of user to true
@app.route('/unsubscribe', methods=['PUT'])
def unsubscribe(user_id=None, tv_show_id=None, function_call=False):
    try:
        if function_call is False:
            data = request.get_json()
            user_id = data['user_id']
            tv_show_id = data['tv_show_id']
        check_slot = UserSlots.query.filter_by(user_id=user_id).filter_by(tv_show_id=tv_show_id).first()

        if check_slot is not None:
            change_subscription_status(user_id, tv_show_id, True)
            db.session.commit()
            return jsonify({'is_success': True,
                            'is_slot_exist': True})
        else:
            return jsonify({'is_success': False,
                            'is_slot_exist:': False})
    except Exception as e:
        return str(e)


# { user_id: [user_id], tv_show_id: [tv_show_id] }
# boolean to convert unsubscribe of user to false
@app.route('/subscribe', methods=['PUT'])
def subscribe(user_id=None, tv_show_id=None, function_call=False):
    try:
        if function_call is False:
            data = request.get_json()
            user_id = data['user_id']
            tv_show_id = data['tv_show_id']
        check_slot = UserSlots.query.filter_by(user_id=user_id).filter_by(tv_show_id=tv_show_id).first()

        if check_slot is not None:
            change_subscription_status(user_id, tv_show_id, False)
            db.session.commit()
            return jsonify({'is_success': True,
                            'is_slot_exist': True})
        else:
            return jsonify({'is_success': False,
                            'is_slot_exist:': False})
    except Exception as e:
        return str(e)


# { user_id: [user_id] }
# route to clear all slots
@app.route('/clear_slots', methods=['PUT'])
def clear_slots():
    try:
        data = request.get_json()
        user_id = data['user_id']
        user_slots_list = UserSlots.query.filter_by(user_id=user_id).all()
        if user_slots_list:
            for user_slots in user_slots_list:
                clear_individual_slot(user_slots.user_id, user_slots.slot_num)
            db.session.commit()
            return jsonify({'slots_cleared': True})
        else:
            return jsonify({'slots_cleared': False})
    except Exception as e:
        return str(e)


# { user_id: [user_id] }
# route to delete a slot only if top slot is empty
@app.route('/delete_slot', methods=['PUT'])
def delete_slot(user_id=None):
    try:
        data = request.get_json()
        user_id = data['user_id']

        user = User.query.filter_by(id=user_id).first()
        top_user_slot = UserSlots.query.filter_by(user_id=user_id).filter_by(slot_num=user.num_slots).first()
        empty_slot = top_user_slot.tv_show_id is None
        more_than_ten_slots = user.num_slots > 10

        if empty_slot and more_than_ten_slots:
            UserSlots.query.filter_by(user_id=user_id).filter_by(slot_num=user.num_slots).delete()
            decrement_slot(user_id)
            db.session.commit()
            return jsonify({'success': True,
                            'more_than_ten_slots': more_than_ten_slots,
                            'empty_slot': empty_slot})
        else:
            return jsonify({'success': False,
                            'more_than_ten_slots': more_than_ten_slots,
                            'empty_slot': empty_slot})

    except Exception as e:
        return str(e)


# [url]/search/user=[email_or_username]
@app.route('/search/user=<query>/page=<int:page>', methods=['GET'])
@app.route('/search/user=/page=<int:page>', methods=['GET'])
@app.route('/search/user=<query>', methods=['GET'])
@app.route('/search/user=', methods=['GET'])
def user_search(query=None, page=1):
    try:
        results = list()
        query_user = '{}%'.format(query)

        # Get all LIKE username
        username_dict = User.query.filter(User.username.like(query_user))
        for user in username_dict:
            results.append(user)

        # Get exact user email
        email_dict = User.query.filter(User.email.like(query_user))
        for user in email_dict:
            if user not in results:
                results.append(user)

        return paginated_json('users', results, page)
    except Exception as e:
        return str(e)


# [url]/users/page=[page]
# [url]/users
@app.route('/users/page=<int:page>', methods=['GET'])
@app.route('/users/page=', methods=['GET'])
@app.route('/users', methods=['GET'])
def get_users(page=1):
    try:
        users = User.query.order_by().all()
        return paginated_json('users', users, page)
    except Exception as e:
        return str(e)


# { request_to: [user_id], request_from: [pending_friend_id] }
# send a friend request to another user
@app.route('/send_friend_request', methods=['POST'])
def send_friend_request():
    try:
        data = request.get_json()
        request_to = data['request_to']
        request_from = data['request_from']

        check_user_to = User.query.filter_by(id=request_to).first()
        check_user_to = check_user_to is not None
        check_user_from = User.query.filter_by(id=request_from)
        check_user_from = check_user_from is not None
        check_friendship = Friends.query.filter_by(user_id=request_from).filter_by(friend_id=request_to).first()
        check_friendship = check_friendship is None
        if check_user_to and check_user_from and check_friendship:
            # add request to table
            new_friend_request = PendingFriends(
                user_id=request_to,
                pending_friend_id=request_from,
            )
            db.session.add(new_friend_request)
            db.session.commit()
            return jsonify({'success': True,
                            'valid_user_to': check_user_to,
                            'valid_user_from': check_user_from,
                            'not_already_friends': check_friendship})
        else:
            return jsonify({'success': False,
                            'valid_user_to': check_user_to,
                            'valid_user_from': check_user_from,
                            'not_already_friends': check_friendship})
    except Exception as e:
        return str(e)


# { user_id: [user_id], request_from: [pending_friend_id] }
# accepts a friend request
@app.route('/accept_friend_request', methods=['POST'])
def accept_friend_request(function_call=False):
    try:
        data = request.get_json()
        user_id = data['request_to']
        pending_friend_id = data['request_from']
        check_user_id = User.query.filter_by(id=user_id).first()
        check_user_id = check_user_id is not None
        check_friend_id = User.query.filter_by(id=pending_friend_id).first()
        check_friend_id = check_friend_id is not None

        # checks for valid inputs
        if check_friend_id and check_user_id:
            check_friend_request = PendingFriends.query.filter_by(user_id=user_id).filter_by(
                pending_friend_id=pending_friend_id).first()
            check_friend_request = check_friend_request is not None
            # checks if friend request exists
            if check_friend_request:
                if function_call is False:
                    add_friend(user_id, pending_friend_id)
                # delete request
                PendingFriends.query.filter_by(user_id=user_id).filter_by(pending_friend_id=pending_friend_id).delete()
                db.session.commit()
                return jsonify({'success': True,
                                'valid_friendship_request': check_friend_request,
                                'valid_user_id': check_user_id,
                                'valid_friend_id': check_friend_id})
            else:
                return jsonify({'success': False,
                                'valid_friendship_request': check_friend_request,
                                'valid_user_id': check_user_id,
                                'valid_friend_id': check_friend_id})
        else:
            return jsonify({'success': False,
                            'valid_friendship_request': False,
                            'valid_user_id': check_user_id,
                            'valid_friend_id': check_friend_id})
    except Exception as e:
        return str(e)


# { user_id: [user_id], pending_friend_id: [pending_friend_id] }
# decline a friend request
@app.route('/decline_friend_request', methods=['POST'])
def decline_friend_request():
    return accept_friend_request(True)


# returns true if user_id and friend_id is in the pending table
# [url]/has_friend_request/user_id=[user_id]/request_from=[pending_friend_id]
@app.route('/has_friend_request/user_id=<int:user_id>/request_from=<int:request_from>', methods=['GET'])
def has_friend_request(user_id=None, request_from=None):
    try:
        if request_from is not None and user_id is not None:
            is_friend_request=PendingFriends.query.filter_by(user_id=user_id).filter_by(pending_friend_id=request_from).scalar()
            if is_friend_request is not None:
                return jsonify({'has_friend_request': True})
            else:
                return jsonify({'has_friend_request': False})
    except Exception as e:
        str(e)


# returns a list of all friend requests from a specific user
# [url]/get_friend_requests/user=[user_id]
@app.route('/get_friend_requests/user=<int:user_id>', methods=['GET'])
@app.route('/get_friend_requests/user=<int:user_id>/page=<int:page>', methods=['GET'])
@app.route('/get_friend_requests/user=/page=', methods=['GET'])
@app.route('/get_friend_requests/user=', methods=['GET'])
def get_friend_requests(user_id=None, page=1):
    try:
        if user_id is not None:
            pending_request_rel = PendingFriends.query.filter_by(user_id=user_id).all()
            pending_friend_list = list()
            for request in pending_request_rel:
                pending_friend = User.query.filter_by(id=request.pending_friend_id).first()
                pending_friend_list.append(pending_friend)

        return paginated_json('pending_friend_requests', pending_friend_list, page)
    except Exception as e:
        return str(e)


# checks if there is at least 1 pending friend request and returns True if there is
# [url]/is_friend_request/user=[user_id]
@app.route('/is_friend_request/user=<int:user_id>', methods=['GET'])
def is_friend_request(user_id=None):
    try:
        friend_request_boolean = False
        if user_id is not None:
            friend_request_boolean = PendingFriends.query.filter_by(user_id=user_id).scalar()
        return jsonify({'at_least_one_request': friend_request_boolean})
    except Exception as e:
        return str(e)


# Check Friendship
# [url]/user1=[user1_id]/user2=[user2_id]
@app.route('/user1=<int:user1_id>/user2=<int:user2_id>')
def is_friend(user1_id=None, user2_id=None, inner_call=False):
    try:
        friendship = Friends.query.filter_by(user_id=user1_id).filter_by(friend_id=user2_id).first()
        if friendship is not None:
            if inner_call:
                return True
            return jsonify({'is_friend': True})
        else:
            if inner_call:
                return False
            return jsonify({'is_friend': False})
    except Exception as e:
        return str(e)


# Display user friends
# [url]/users=[user_id]/friends/page=[page]
# [url]/users=[user_id]/friends
@app.route('/user=<int:user_id>/friends/page=<int:page>', methods=['GET'])
@app.route('/user=<int:user_id>/friends/page=', methods=['GET'])
@app.route('/user=<int:user_id>/friends', methods=['GET'])
def get_user_friend_list(user_id=None, page=1):
    try:
        friend_list = list()

        # Ensure Valid User ID
        user = User.query.filter_by(id=user_id).first()
        if user is not None:
            # Get list of all entries with the User's ID
            friends = Friends.query.filter_by(user_id=user_id)

            # Create list of the user's friend's IDs
            friend_ids = list()
            for friend in friends:
                if friend.friend_id is not user_id:
                    friend_ids.append(friend.friend_id)

            # Append the Users that match the friend IDs
            for friend_id in friend_ids:
                friend_list.append(User.query.filter_by(id=friend_id).first())

        return paginated_json('friends', friend_list, page)

    except Exception as e:
        return str(e)


# [url]/user=[user_id]/friends/remove=[friend_id]
@app.route('/user=<int:user_id>/friends/remove=<int:friend_id>', methods=['DELETE'])
def remove_friend(user_id=None, friend_id=None):
    try:
        friend = User.query.filter_by(id=friend_id).first()

        if friend is None or user_id is None or friend_id is None:
            return jsonify({'user_exist': False, 'friend_exist': False, 'friend_deleted': False})
        else:
            relationship = Friends.query.filter_by(user_id=user_id).filter_by(friend_id=friend_id).first()

            if relationship is None:
                return jsonify({'user_exist': True, 'friend_exist': False, 'friend_deleted': False})
            else:
                Friends.query.filter_by(user_id=user_id).filter_by(friend_id=friend_id).delete()
                Friends.query.filter_by(user_id=friend_id).filter_by(friend_id=user_id).delete()
                db.session.commit()
                return jsonify({'user_exist': True, 'friend_exist': True, 'friend_deleted': True})

    except Exception as e:
        return str(e)


# Display user's slots
# [url]/user=[user_id]/slots
@app.route('/user=<int:user_id>/slots', methods=['GET'])
def get_user_slots(user_id=None):
    try:
        # Ensure Valid User ID
        user = User.query.filter_by(id=user_id).first()
        if user is not None:
            # Get list of all entries with the User's ID
            user_slots = UserSlots.query.filter_by(user_id=user_id)

            slot_info = list()
            for user_slot in user_slots:
                if user_slot.tv_show_id is None:
                    slot = Slot(user_slot.slot_num, None, None)
                else:
                    tv_show = TVShows.query.filter_by(id=user_slot.tv_show_id).first()
                    slot = Slot(user_slot.slot_num, tv_show.title, tv_show.image_url)
                slot_info.append(slot)

            result = DisplayUserSlots(slot_info)
            return jsonify({'user_slots': result.serialize()})

    except Exception as e:
        return str(e)


# [url]/users=[user_id]/movie_list
@app.route('/user=<int:user_id>/movie_list', methods=['GET'])
def get_user_movie_list(user_id=None):
    try:
        user_rated_movies = list()

        # Ensure Valid User ID
        user = User.query.filter_by(id=user_id).first()
        if user is not None:
            rated_movies = list()

            # Get list of all entries with the User's ID
            rated_movie_entry = UserRatedMovieRel.query.filter_by(user_id=user_id)

            # Append the User Rated Movies
            for rm_entry in rated_movie_entry:
                movie = Movie.query.filter_by(id=rm_entry.movie_id).first()
                movie_id = movie.id
                title = movie.title
                image_url = movie.image_url
                rating = rm_entry.user_rating

                rm = RatedMovie(movie_id, title, image_url, rating)
                rated_movies.append(rm)

            user_rated_movies = DisplayRatedMovie(user.id, rated_movies)

        return jsonify({'movie_list': user_rated_movies.serialize()})

    except Exception as e:
        return str(e)


# [url]/user=[user_id]/movie=[movie_id]/rating
@app.route('/user=<user_id>/movie=<movie_id>/rating', methods=['GET'])
def get_user_movie_rating(user_id=None, movie_id=None):
    try:
        entry = UserRatedMovieRel.query.filter_by(user_id=user_id).filter_by(movie_id=movie_id).first()
        return jsonify({'movie_rating': entry.user_rating})
    except Exception as e:
        return str(e)


# { user_id: [user_id], movie_id: [movie_id], rating: [1-5] }
# [url]/rate/movie
@app.route('/user/movie/rating', methods=['POST'])
def rate_movie():
    try:
        data = request.get_json()
        user_id = data['user_id']
        movie_id = data['movie_id']
        rating = data['rating']

        user = User.query.filter_by(id=user_id).first()
        movie = Movie.query.filter_by(id=movie_id).first()
        user_rated_movie = UserRatedMovieRel.query.filter_by(user_id=user_id).filter_by(movie_id=movie_id).first()

        if user is None and movie is None:
            return jsonify({'valid_user': False, 'valid_movie': False, 'success': False})
        elif user is None:
            return jsonify({'valid_user': False, 'valid_movie': True, 'success': False})
        elif movie is None:
            return jsonify({'valid_user': True, 'valid_movie': False, 'success': False})

        # First Time Rating Movie
        elif user_rated_movie is None:
            new_rated_movie = UserRatedMovieRel(
                user_id=user_id,
                movie_id=movie_id,
                user_rating=rating,
            )
            db.session.add(new_rated_movie)
            db.session.commit()
            update_average_rating(False, movie_id)
            return jsonify({'valid_user': True, 'valid_movie': True, 'success': True})

        # Updating Their current Rating
        else:
            user_rated_movie.user_rating = rating
            db.session.commit()
            update_average_rating(False, movie_id)
            return jsonify({'valid_user': True, 'valid_movie': True, 'success': True})
    except Exception as e:
        return str(e)


@app.route('/movie/comment', methods=['POST'])
def comment_movie():
    try:
        data = request.get_json()
        user_id = data['user_id']
        movie_id = data['movie_id']
        comment = data['comment']
        date_of_comment = str(datetime.now())

        user = User.query.filter_by(id=user_id).first()
        movie = Movie.query.filter_by(id=movie_id).first()

        if user is None and movie is None:
            return jsonify({'valid_user': False, 'valid_movie': False, 'success': False})
        elif user is None:
            return jsonify({'valid_user': False, 'valid_movie': True, 'success': False})
        elif movie is None:
            return jsonify({'valid_user': True, 'valid_movie': False, 'success': False})
        else:
            user_comment = MovieComment(
                user_id=user_id,
                movie_id=movie_id,
                comment=comment,
                date_of_comment=date_of_comment,
            )
            db.session.add(user_comment)
            db.session.commit()
            return jsonify({'valid_user': True, 'valid_movie': True, 'success': True})
    except Exception as e:
        return str(e)


# Chronological Movie Comments
# [url]/movie=[title]/comments
@app.route('/movie=<title>/comments/reverse=<reverse>', methods=['GET'])
@app.route('/movie=<title>/comments', methods=['GET'])
def get_movie_comments(title=None, reverse=False):
    try:
        movie = Movie.query.filter_by(title=title).first()

        if movie is None:
            return jsonify({'valid_movie': False})
        else:
            comments = list()
            raw_comments = MovieComment.query.filter_by(movie_id=movie.id).order_by(MovieComment.date_of_comment)

            for rc in raw_comments:
                user_id = rc.user_id
                username = User.query.filter_by(id=user_id).first().username
                comment = rc.comment
                date_of_comment = rc.date_of_comment
                comments.append(Comment(
                    user_id=user_id,
                    username=username,
                    comment=comment,
                    date_of_comment=date_of_comment,
                ))

            if reverse:
                comments = reversed(comments)

            return jsonify({'comments': [comment.serialize() for comment in comments]})

    except Exception as e:
        return str(e)


# [url]/user=[user_id]/tv_show=[tv_show_id]/rating
@app.route('/user=<user_id>/tv_show=<tv_show_id>/rating', methods=['GET'])
def get_user_tv_show_rating(user_id=None, tv_show_id=None):
    try:
        entry = UserRatedTVShowRel.query.filter_by(user_id=user_id).filter_by(tv_show_id=tv_show_id).first()
        return jsonify({'tv_show_rating': entry.user_rating})
    except Exception as e:
        return str(e)


# { user_id: [user_id], tv_show_id: [tv_show_id], rating: [1-5] }
# [url]/tv_show/rating
@app.route('/user/tv_show/rating', methods=['POST'])
def rate_tv_show():
    try:
        data = request.get_json()
        tv_show_id = data['tv_show_id']
        user_id = data['user_id']
        rating = data['rating']

        user = User.query.filter_by(id=user_id).first()
        tv_show = TVShows.query.filter_by(id=tv_show_id).first()
        user_rated_tv_show = UserRatedTVShowRel.query.filter_by(user_id=user_id).filter_by(
            tv_show_id=tv_show_id).first()

        if user is None and tv_show is None:
            return jsonify({'valid_user': False, 'valid_tv_show': False, 'success': False})
        elif user is None:
            return jsonify({'valid_user': False, 'valid_tv_show': True, 'success': False})
        elif tv_show is None:
            return jsonify({'valid_user': True, 'valid_tv_show': False, 'success': False})

        # First Time Rating TV Show
        elif user_rated_tv_show is None:
            new_rated_tv_show = UserRatedTVShowRel(
                user_id=user_id,
                tv_show_id=tv_show_id,
                user_rating=rating,
            )
            db.session.add(new_rated_tv_show)
            db.session.commit()
            update_average_rating(True, tv_show_id)
            return jsonify({'valid_user': True, 'valid_tv_show': True, 'success': True})

        # Updating Their current Rating
        else:
            user_rated_tv_show.user_rating = rating
            db.session.commit()
            update_average_rating(True, tv_show_id)
            return jsonify({'valid_user': True, 'valid_tv_show': True, 'success': True})
    except Exception as e:
        return str(e)


# { user_id: [user_id], tv_show_id: [tv_show_id], comment: [comment] }
# [url]/tv_show/comment
@app.route('/tv_show/comment', methods=['POST'])
def comment_tv_show():
    try:
        data = request.get_json()
        tv_show_id = data['tv_show_id']
        user_id = data['user_id']
        comment = data['comment']
        date_of_comment = str(datetime.now())

        user = User.query.filter_by(id=user_id).first()
        tv_show = TVShows.query.filter_by(id=tv_show_id).first()

        if user is None and tv_show is None:
            return jsonify({'valid_user': False, 'valid_tv_show': False, 'success': False})
        elif user is None:
            return jsonify({'valid_user': False, 'valid_tv_show': True, 'success': False})
        elif tv_show is None:
            return jsonify({'valid_user': True, 'valid_tv_show': False, 'success': False})
        else:
            user_comment = TVShowComment(
                tv_show_id=tv_show_id,
                user_id=user_id,
                comment=comment,
                date_of_comment=date_of_comment,
            )
            db.session.add(user_comment)
            db.session.commit()
            return jsonify({'valid_user': True, 'valid_tv_show': True, 'success': True})
    except Exception as e:
        return str(e)


# Chronological TV Show Comments
# [url]/tv_show=[title]/comments
@app.route('/tv_show=<title>/comments/reverse=<reverse>', methods=['GET'])
@app.route('/tv_show=<title>/comments', methods=['GET'])
def get_tv_show_comments(title=None, reverse=False):
    try:
        tv_show = TVShows.query.filter_by(title=title).first()

        if tv_show is None:
            return jsonify({'valid_tv_show': False})
        else:
            comments = list()
            raw_comments = TVShowComment.query.filter_by(tv_show_id=tv_show.id).order_by(TVShowComment.date_of_comment)

            for rc in raw_comments:
                user_id = rc.user_id
                username = User.query.filter_by(id=user_id).first().username
                comment = rc.comment
                date_of_comment = rc.date_of_comment
                comments.append(Comment(
                    user_id=user_id,
                    username=username,
                    comment=comment,
                    date_of_comment=date_of_comment,
                ))

            if reverse:
                comments = reversed(comments)

            return jsonify({'comments': [comment.serialize() for comment in comments]})

    except Exception as e:
        return str(e)


# [url]/users=[user_id]/tv_show_list
@app.route('/user=<int:user_id>/tv_show_list', methods=['GET'])
def get_user_tv_show_list(user_id=None):
    try:
        user_rated_tv_shows = list()

        # Ensure Valid User ID
        user = User.query.filter_by(id=user_id).first()
        if user is not None:
            rated_tv_shows = list()

            # Get list of all entries with the User's ID
            rated_tv_show_entry = UserRatedTVShowRel.query.filter_by(user_id=user_id)

            # Append the User Rated TV Shows
            for rts_entry in rated_tv_show_entry:
                tv_show = TVShows.query.filter_by(id=rts_entry.tv_show_id).first()
                tv_id = tv_show.id
                title = tv_show.title
                image_url = tv_show.image_url
                rating = rts_entry.user_rating

                rts = RatedTVShow(tv_id, title, image_url, rating)
                rated_tv_shows.append(rts)

            user_rated_tv_shows = DisplayRatedTVShow(user.id, rated_tv_shows)

        return jsonify({'tv_show_list': user_rated_tv_shows.serialize()})

    except Exception as e:
        return str(e)


# [url]/user=[user_id]/movie=[movie_id]/is_movie_rented
@app.route('/user=<user_id>/movie=<movie_id>/is_movie_rented', methods=['GET'])
@app.route('/user=/movie=/is_movie_rented', methods=['GET'])
def is_movie_rented(user_id=None, movie_id=None):
    try:
        if UserRentedMovies.query.filter_by(user_id=user_id).filter_by(movie_id=movie_id).first() is not None:
            return jsonify({'is_movie_rented': True})
        else:
            return jsonify({'is_movie_rented': False})
    except Exception as e:
        return str(e)


@app.route('/user=<int:user_id>/rented_movies', methods=['GET'])
def get_user_rented_movies(user_id=None):
    try:
        movies = list()
        user_movie_rel = UserRentedMovies.query.filter_by(user_id=user_id).all()
        for user_movie in user_movie_rel:
            movies.append(Movie.query.filter_by(id=user_movie.movie_id).first())

        return jsonify({'user_rented_movies': [movie.serialize() for movie in movies]})

    except Exception as e:
        return str(e)


# { user_id: [user_id], movie_id: [movie_id] }
# adds rented movie into user_rented_movies table
@app.route('/rent_movie', methods=['POST'])
def rent_movie():
    data = request.get_json()
    user_id = data['user_id']
    movie_id = data['movie_id']
    rent_datetime = datetime.now()

    user_check = User.query.filter_by(id=user_id).first()
    movie_check = Movie.query.filter_by(id=movie_id).first()

    # checks if data is valid
    if user_check is None and movie_check is None:
        return jsonify({'success': False,
                        'valid_user': False,
                        'valid_movie': False})
    elif user_check is None:
        return jsonify({'success': False,
                        'valid_user': False,
                        'valid_movie': True})
    elif movie_check is None:
        return jsonify({'success': False,
                        'valid_user': True,
                        'valid_movie': False})

    try:
        user_rented_movies = UserRentedMovies(
            user_id=user_id,
            movie_id=movie_id,
            rent_datetime=rent_datetime
        )
        db.session.add(user_rented_movies)
        db.session.commit()
        return jsonify({'success': True,
                        'valid_user': True,
                        'valid_movie': True})
    except Exception as e:
        return str(e)


# add friend friend and friend adds back
def add_friend(user_id, friend_id):
    try:
        # Add friend to database
        friend = Friends(
            user_id=user_id,
            friend_id=friend_id
        )
        db.session.add(friend)

        # Friend adds back
        friend_back = Friends(
            user_id=friend_id,
            friend_id=user_id
        )
        db.session.add(friend_back)
        return 'success'
    except Exception as e:
        return str(e)


# [url]/user=[user_id]/wall
@app.route('/user=<user_id>/wall', methods=['GET'])
def display_wall(user_id=None):
    try:
        wall = list()
        user = User.query.filter_by(id=user_id).first()

        wall_posts = TimeLine.query.filter_by(user_id=user.id).order_by(TimeLine.date_of_post)

        for post in wall_posts:
            username = User.query.filter_by(id=post.user_id).first().username
            post_username = User.query.filter_by(id=post.post_user_id).first().username

            comments = list()
            comment_list = PostComments.query.filter_by(user_id=post.user_id).filter_by(
                post_user_id=post.post_user_id).filter_by(post_id=post.post_id)
            for comment in comment_list:
                comment_username = User.query.filter_by(id=comment.comment_user_id).first().username
                comments.append(PostComment(
                    username=username,
                    post_username=post_username,
                    comment_username=comment_username,
                    comment=comment.comment,
                    date_of_comment=comment.date_of_comment,
                ))

            wall.append(Post(
                username=username,
                post_username=post_username,
                post=post.post,
                date_of_post=post.date_of_post,
                comments=reversed(comments),
            ))

        wall.sort(key=lambda w: w.date_of_post)
        wall = reversed(wall)

        return jsonify({'wall': [w.serialize() for w in wall]})

    except Exception as e:
        return str(e)


# [url]/user=[user_id]/timeline
@app.route('/user=<user_id>/timeline', methods=['GET'])
def display_timeline(user_id=None):
    try:
        timeline = list()
        user = User.query.filter_by(id=user_id).first()
        friend_list = Friends.query.filter_by(user_id=user_id)

        # View All Self and Friend Walls
        for friend in friend_list:
            friend_wall = TimeLine.query.filter_by(user_id=friend.friend_id).order_by(TimeLine.date_of_post)

            for post in friend_wall:
                username = User.query.filter_by(id=post.user_id).first().username
                post_username = User.query.filter_by(id=post.post_user_id).first().username

                comments = list()
                comment_list = PostComments.query.filter_by(user_id=post.user_id).filter_by(
                    post_user_id=post.post_user_id).filter_by(post_id=post.post_id)
                for comment in comment_list:
                    comment_username = User.query.filter_by(id=comment.comment_user_id).first().username
                    comments.append(PostComment(
                        username=username,
                        post_username=post_username,
                        comment_username=comment_username,
                        comment=comment.comment,
                        date_of_comment=comment.date_of_comment,
                    ))

                timeline.append(Post(
                    username=username,
                    post_username=post_username,
                    post=post.post,
                    date_of_post=post.date_of_post,
                    comments=reversed(comments),
                ))

        timeline.sort(key=lambda tl: tl.date_of_post)
        timeline = reversed(timeline)

        return jsonify({'timeline': [tl.serialize() for tl in timeline]})

    except Exception as e:
        return str(e)


# { "user_id": [user_id], "post_user_id": [post_user_id], "post": [post_text] }
# [url]/timeline/post
@app.route('/timeline/post', methods=['POST'])
def post_timeline():
    try:
        data = request.get_json()
        user_id = data['user_id']
        post_user_id = data['post_user_id']
        post = data['post']
        date_of_post = datetime.now()

        if User.query.filter_by(id=user_id).first() is None:
            return jsonify({'success': False,
                            'valid_user': False,
                            'valid_friend': False})

        # Can only post if friend
        if is_friend(user_id, post_user_id, True):
            timeline = TimeLine(user_id=user_id,
                                post_user_id=post_user_id,
                                post=post,
                                date_of_post=date_of_post)
            db.session.add(timeline)
            db.session.commit()

            return jsonify({'success': True,
                            'valid_user': True,
                            'valid_friend': True})
        else:
            return jsonify({'success': False,
                            'valid_user': True,
                            'valid_friend': False})
    except Exception as e:
        return str(e)


# { "user_id": [user_id], "post_user_id": [post_user_id], "comment_user_id": [comment_user_id', "comment": [comment_text] }
# [url]/timeline/post/comment
@app.route('/timeline/post/comment', methods=['POST'])
def comment_on_post():
    try:
        data = request.get_json()
        user_id = data['user_id']
        post_user_id = data['post_user_id']
        comment_user_id = data['comment_user_id']
        comment = data['comment']
        date_of_comment = datetime.now()
        post_id = data['post_id']

        if User.query.filter_by(id=user_id).first() is None:
            return jsonify({'success': False,
                            'valid_user': False,
                            'valid_friend': False,
                            'valid_post_id': False})

        elif PostComments.query.filter_by(post_id=post_id).first() is None:
            return jsonify({'success': False,
                            'valid_user': True,
                            'valid_friend': False,
                            'valid_post_id': False})

        # Can only post if friend
        if is_friend(user_id, post_user_id, True) and is_friend(user_id, comment_user_id, True):

            post_comment = PostComments(user_id=user_id,
                                        post_user_id=post_user_id,
                                        comment_user_id=comment_user_id,
                                        comment=comment,
                                        date_of_comment=date_of_comment,
                                        post_id=post_id)
            db.session.add(post_comment)
            db.session.commit()

            return jsonify({'success': True,
                            'valid_user': True,
                            'valid_friend': True,
                            'valid_post_id': True})
        else:
            return jsonify({'success': False,
                            'valid_user': True,
                            'valid_friend': False,
                            'valid_post_id': True})

    except Exception as e:
        return str(e)


def update_average_rating(is_tv_show: bool, media_id: int):
    try:
        if is_tv_show:
            average = get_average_rating(True, media_id)
            tv_show = TVShows.query.filter_by(id=media_id).first()
            tv_show.avg_rating = average
            db.session.commit()

        else:
            average = get_average_rating(False, media_id)
            movie = Movie.query.filter_by(id=media_id).first()
            movie.avg_rating = average
            db.session.commit()

    except Exception as e:
        return str(e)


def get_average_rating(is_tv_show: bool, media_id: int):
    try:
        if is_tv_show:
            tv_show_ratings = UserRatedTVShowRel.query.filter_by(tv_show_id=media_id)
            total = 0
            num_ratings = 0

            for tsr in tv_show_ratings:
                total += tsr.user_rating
                num_ratings += 1
            return '%.2f' % (total / num_ratings)

        else:
            movie_ratings = UserRatedMovieRel.query.filter_by(movie_id=media_id)
            total = 0
            num_ratings = 0

            for mr in movie_ratings:
                total += mr.user_rating
                num_ratings += 1

            return '%.2f' % (total / num_ratings)

    except Exception as e:
        return str(e)


# checks database if movies are past rented due date and deletes them
def delete_expired_movies():
    try:
        yesterday_datetime = datetime.now() - timedelta(1)

        # ensures list is not empty
        check_not_empty = UserRentedMovies.query.filter(UserRentedMovies.rent_datetime <= yesterday_datetime)
        if check_not_empty:
            UserRentedMovies.query.filter(UserRentedMovies.rent_datetime <= yesterday_datetime).delete()
            db.session.commit()
            return 'success'
        else:
            return 'no movies to delete'

    except Exception as e:
        return str(e)


# need to add to login function and need to add check to not allow deleting slots past 10
def delete_expired_tv_shows():
    try:
        month_ago_date = (datetime.now() - timedelta(30)).date()
        # ensures list is not empty
        expired_users = User.query.filter(User.sub_date <= month_ago_date)

        if expired_users:
            for user in expired_users:
                remove_list = UserSlots.query.filter_by(user_id=user.id).filter_by(unsubscribe=True)
                update_sub_date(user.id)
                email_sender.subscription_renew_email(user.username, user.email, user.sub_date + timedelta(30))
                for tv_show_to_remove in remove_list:
                    subscribe(user.id, tv_show_to_remove.tv_show_id, True)
                    remove_tv_show(user.id, tv_show_to_remove.tv_show_id)
            db.session.commit()
            return jsonify({'expired_tv_shows_removed': True})
        else:
            return jsonify({'expired_tv_shows_removed': False})

    except Exception as e:
        return str(e)


# updates user's resub date by adding 30 days
def update_sub_date(user_id=None):
    # increment slot number in users
    check_id = User.query.filter_by(id=user_id).first()

    name = check_id.name
    username = check_id.username
    email = check_id.email
    password = check_id.password
    card_num = check_id.card_num
    num_slots = check_id.num_slots
    sub_date = check_id.sub_date + timedelta(30)

    try:
        user = User.query.filter_by(id=user_id).first()
        user.id = user_id
        user.name = name
        user.username = username
        user.email = email
        user.password = password
        user.card_num = card_num
        user.num_slots = num_slots
        user.sub_date = sub_date

        return 'sucess'

    except Exception as e:
        return str(e)


# adds an empty slot to user_slots in database
def add_empty_slot(user_id, slot_num):
    user_slots = UserSlots(
        user_id=user_id,
        slot_num=slot_num,
        tv_show_id=None,
        unsubscribe=False,
    )
    db.session.add(user_slots)
    db.session.commit()
    return "user_slots added"


# route to delete tv_show in slot
def remove_tv_show(user_id=None, tv_show_id=None):
    try:
        # get slot_num of deleted tv show
        deletion_index = UserSlots.query.filter_by(user_id=user_id).filter_by(tv_show_id=tv_show_id).first()
        deletion_index = deletion_index.slot_num

        # shift all the values in the database back one
        user_slots = UserSlots.query.filter_by(user_id=user_id).all()
        previous_slot = None
        for slot in user_slots:
            if slot.slot_num > deletion_index:
                previous_slot.user_id = user_id
                previous_slot.slot_num = previous_slot.slot_num
                previous_slot.tv_show_id = slot.tv_show_id
            previous_slot = slot
            if slot.slot_num == len(user_slots):
                clear_individual_slot(user_id, slot.slot_num)
        return jsonify({'tv_show_deleted': True})

    except Exception as e:
        return str(e)


# (Pseudo PUT) increment user's slot_num by 1 and return new slot_id
def increment_slot(user_id) -> int:
    # increment slot number in users
    check_id = User.query.filter_by(id=user_id).first()

    name = check_id.name
    username = check_id.username
    email = check_id.email
    password = check_id.password
    card_num = check_id.card_num
    num_slots = check_id.num_slots + 1
    sub_date = check_id.sub_date
    profile_pic = check_id.profile_pic

    try:
        user = User.query.filter_by(id=user_id).first()
        user.id = user_id
        user.name = name
        user.username = username
        user.email = email
        user.password = password
        user.card_num = card_num
        user.num_slots = num_slots
        user.sub_date = sub_date
        user.profile_pic = profile_pic

        return num_slots

    except Exception as e:
        return str(e)


# (Pseudo PUT) increment user's slot_num by 1 and return new slot_id
def decrement_slot(user_id) -> int:
    # increment slot number in users
    check_id = User.query.filter_by(id=user_id).first()

    name = check_id.name
    username = check_id.username
    email = check_id.email
    password = check_id.password
    card_num = check_id.card_num
    num_slots = check_id.num_slots - 1
    sub_date = check_id.sub_date
    profile_pic = check_id.profile_pic

    try:
        user = User.query.filter_by(id=user_id).first()
        user.id = user_id
        user.name = name
        user.username = username
        user.email = email
        user.password = password
        user.card_num = card_num
        user.num_slots = num_slots
        user.sub_date = sub_date
        user.profile_pic = profile_pic

        return num_slots

    except Exception as e:
        return str(e)


def clear_individual_slot(user_id, slot_num):
    try:
        check_slot_id = UserSlots.query.filter_by(user_id=user_id).filter_by(slot_num=slot_num).first()
        if check_slot_id is not None:
            check_slot_id.user_id = user_id
            check_slot_id.slot_id = slot_num
            check_slot_id.tv_show_id = None
            return 'success'
    except Exception as e:
        return str(e)


def change_subscription_status(user_id, tv_show_id, unsubscribe_boolean):
    # increment slot number in users

    try:
        user_slot = UserSlots.query.filter_by(user_id=user_id).filter_by(tv_show_id=tv_show_id).first()

        user_slot.user_id = user_id
        user_slot.slot_num = user_slot.slot_num
        user_slot.tv_show_id = tv_show_id
        user_slot.unsubscribe = unsubscribe_boolean

        return 'success'

    except Exception as e:
        return str(e)


# Pseudo Pagination
def pseudo_paginate(page: int, list_to_paginate: []):
    start_page = (page - 1) * app.config['POSTS_PER_PAGE']
    end_page = start_page + app.config['POSTS_PER_PAGE']
    if end_page > len(list_to_paginate):
        end_page = len(list_to_paginate)

    return list_to_paginate[start_page:end_page]


# Return Paginated json
def paginated_json(json_name: str, queried_results: [], page: int):
    num_pages = max_pages(queried_results)

    # Paginate results
    results = pseudo_paginate(page, queried_results)

    json = make_response(jsonify({json_name: [result.serialize() for result in results]}))
    json.headers['current_page'] = page
    json.headers['max_pages'] = num_pages

    # Headers the Client is Allowed to Access
    json.headers['Access-Control-Expose-Headers'] = 'current_page, max_pages'
    return json


# Return max pages for specified query
def max_pages(queried_list: []):
    return int(math.ceil(len(queried_list) / app.config['POSTS_PER_PAGE']))


if __name__ == '__main__':
    app.run(port=port)
