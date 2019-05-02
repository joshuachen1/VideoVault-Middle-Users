# -*- coding: utf-8 -*-
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
app.config.from_object('config.TestingConfig')  # Should change based on is in Development or Production
# app.config.from_object(os.environ['APP_SETTINGS'])  # Should change based on is in Development or Production
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
from models.Email import Email
from models.crypto_models import Key
from models.user_models import Login
from models.user_models import User, Friends, PendingFriends
from models.user_models import TimeLine, Post, PostComments, PostComment
from models.user_models import Slot, UserSlots, DisplayUserSlots, UserRentedMovies
from models.user_models import UserRatedMovieRel, DisplayRatedMovie, RatedMovie
from models.user_models import UserRatedTVShowRel, DisplayRatedTVShow, RatedTVShow
from models.user_media_models import Movie, MovieComment, TVShows, TVShowComment, Comment

# Set Up Email Server
email_sender = Email(app.config['COMPANY_EMAIL'])


# [url]/
@app.route('/')
def hello_world():
    return 'Home Page'


# { name: [name], username: [username], email:[email], password: [password], card_num: [card_num] }
# adds user to user table and creates 10 slots in user_slots
@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        name = data['name']
        username = data['username']
        email = data['email']
        password = data['password']
        card_num = data['card_num']
        num_slots = 10
        sub_date = str(date.today())
        profile_pic = "https://upload.wikimedia.org/wikipedia/en/1/13/Stick_figure.png"

        if (name is None or name is '') and \
                (username is None or username is '') and \
                (email is None or email is '') and \
                (password is None or password is '') and \
                (card_num is None or not isinstance(card_num, int)):
            return jsonify({
                'valid_name': False,
                'valid_username': False,
                'username_taken': False,
                'valid_email': False,
                'email_taken': False,
                'valid_password': False,
                'valid_card_num': False,
                'success': False
            })

        if name is None or name is '':
            return jsonify({
                'valid_name': False,
                'valid_username': False,
                'username_taken': False,
                'valid_email': False,
                'email_taken': False,
                'valid_password': False,
                'valid_card_num': False,
                'success': False
            })

        if username is not None or username is '':
            # Check if username exists
            check_unique = User.query.filter_by(username=username).first()
            if check_unique is not None:
                return jsonify({
                    'valid_name': True,
                    'valid_username': True,
                    'username_taken': True,
                    'valid_email': False,
                    'email_taken': False,
                    'valid_password': False,
                    'valid_card_num': False,
                    'success': False
                })

        # Check if @ sign and period after @ sign
        email_pattern = re.compile("[^@]+@[^@]+\.[^@]+")
        if email is None or email is '' or email_pattern.match(email) is None:
            return jsonify({
                'valid_name': True,
                'valid_username': True,
                'username_taken': False,
                'valid_email': False,
                'email_taken': False,
                'valid_password': False,
                'valid_card_num': False,
                'success': False
            })

        # Check if email exists
        check_unique = User.query.filter_by(email=email).first()
        if email is None or email is '' or check_unique is not None:
            return jsonify({
                'valid_name': True,
                'valid_username': True,
                'username_taken': False,
                'valid_email': True,
                'email_taken': True,
                'valid_password': False,
                'valid_card_num': False,
                'success': False
            })

        if password is None or password is '':
            return jsonify({
                'valid_name': True,
                'valid_username': True,
                'username_taken': False,
                'valid_email': True,
                'email_taken': False,
                'valid_password': False,
                'valid_card_num': False,
                'success': False
            })

        if card_num is None or not isinstance(card_num, int):
            return jsonify({
                'valid_name': True,
                'valid_username': True,
                'username_taken': False,
                'valid_email': True,
                'email_taken': False,
                'valid_password': True,
                'valid_card_num': False,
                'success': False
            })
        elif not len(str(card_num)) == 16:
            return jsonify({
                'valid_name': True,
                'valid_username': True,
                'username_taken': False,
                'valid_email': True,
                'email_taken': False,
                'valid_password': True,
                'valid_card_num': False,
                'success': False
            })

        # Get Key
        key = Key.query.filter_by(id=1).first().key
        key = key.encode('utf-8')
        cipher = Fernet(key)

        # Encrypt User Password
        password = password.encode('utf-8')
        encrypted_pwd = cipher.encrypt(password)

        # Encrypt User Credit Card Number
        card_num = str(card_num)
        card_num = card_num.encode('utf-8')
        encrypted_cn = cipher.encrypt(card_num)
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


# [url]/login/email=[email]/password=[password]
@app.route('/login/email=<email>/password=<attempted_pwd>', methods=['GET'])
@app.route('/login/email=<email>/password=', methods=['GET'])
@app.route('/login/email=/password=<attempted_pwd>', methods=['GET'])
@app.route('/login/email=/password=', methods=['GET'])
def login(email=None, attempted_pwd=None):
    user_info = User.query.filter_by(email=email).first()

    if (email is None or email is '') and (user_info is None) and (attempted_pwd is None or attempted_pwd is ''):
        result = Login(True, True, False)
        return jsonify(result.serialize())
    elif email is None or email is '':
        result = Login(True, False, False)
        return jsonify(result.serialize())
    elif attempted_pwd is None or attempted_pwd is '':
        result = Login(False, True, False)
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
        user = User.query.filter_by(email=email).first()
        database_update(True, user.id)
        return jsonify(user_info.serialize())
    else:
        result = Login(False, True, False)
        return jsonify(result.serialize())


# { user_id: [user_id], tv_show_id: [tv_show_id_list] }
# fills all slots with tv shows into user_slots table
@app.route('/resub', methods=['PUT'])
def resub():
    try:
        data = request.get_json()
        user_id = data['user_id']
        tv_show_ids = data['tv_show_id']

        user_check = User.query.filter_by(id=user_id).scalar()

        # creating booleans
        is_success = True
        is_valid_user = True
        is_valid_tv_show = True
        is_valid_number_of_tv_shows = True

        # return boolean for invalid inputs
        if user_check is None:
            is_success = False
            is_valid_user = False
        if tv_show_ids is None or not isinstance(tv_show_ids, list):
            is_success = False
            is_valid_tv_show = False
            is_valid_number_of_tv_shows = False
        else:
            if is_valid_user is False or len(tv_show_ids) is not user_check.num_slots:
                is_success = False
                is_valid_number_of_tv_shows = False
            if len(tv_show_ids) != len(set(tv_show_ids)):
                is_success = False
                is_valid_tv_show = False
            for tv_show_id in tv_show_ids:
                if tv_show_id is None or not str(tv_show_id).isdigit() or tv_show_id <= 0:
                    is_success = False
                    is_valid_tv_show = False
                    break
                elif TVShows.query.filter_by(id=tv_show_id).scalar() is None:
                    is_success = False
                    is_valid_tv_show = False
                    break

        # return json response if any of these tests failed
        if is_success is False:
            return jsonify({'success': is_success,
                            'valid_user': is_valid_user,
                            'valid_tv_shows': is_valid_tv_show,
                            'valid_number_of_tv_shows': is_valid_number_of_tv_shows})
        # add each entry to the user_slots table
        for slot_num in range(len(tv_show_ids)):
            add_tv_show(True, slot_num + 1, tv_show_ids[slot_num], user_id)
        db.session.commit()

        email_sender.subscription_renew_email(User.query.filter_by(id=user_id).first().username,
                                              User.query.filter_by(id=user_id).first().email,
                                              User.query.filter_by(id=user_id).first().sub_date + timedelta(30))
        return jsonify({'success': is_success,
                        'valid_user': is_valid_user,
                        'valid_tv_shows': is_valid_tv_show,
                        'valid_number_of_tv_shows': is_valid_number_of_tv_shows
                        })
    except Exception as e:
        return str(e)


# Need User Id and Password
@app.route('/account/delete', methods=['DELETE'])
def delete_account():
    try:
        data = request.get_json()
        user_id = data['user_id']
        password = data['password']

        if (user_id is None or user_id is '') and (password is None or password is ''):
            return jsonify({'success': False,
                            'valid_user': False})
        elif user_id is None or user_id is '':
            return jsonify({'success': False,
                            'valid_user': False})

        user = User.query.filter_by(id=user_id).first()

        # Get Key
        key = Key.query.filter_by(id=1).first().key
        key = key.encode('utf-8')
        cipher = Fernet(key)

        # Check Matching Password
        true_pwd = user.password.encode('utf-8')
        decrypted_pwd = (cipher.decrypt(true_pwd)).decode('utf-8')

        if decrypted_pwd != password:
            return jsonify({'success': False,
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
            UserRatedMovieRel.query.filter_by(user_id=user_id).delete()
            UserRatedTVShowRel.query.filter_by(user_id=user_id).delete()

            # Remove All User Slots
            UserSlots.query.filter_by(user_id=user_id).delete()

            # Remove From User Table
            User.query.filter_by(id=user_id).delete()

            db.session.commit()

            return jsonify({'success': True,
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

        if (user is None or user_id is '' or user_id is None) and (profile_pic is '' or profile_pic is None):
            return jsonify({'success': False,
                            'valid_user': False,
                            'valid_pic': False})
        elif user is None or user_id is None or user_id is '':
            return jsonify({'success': False,
                            'valid_user': False,
                            'valid_pic': True})
        elif profile_pic is None or profile_pic is '':
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
    if user_id is not None and user_id.isdigit():
        user_id = int(user_id)
    if user_id is None or not isinstance(user_id, int):
        return jsonify({'is_slots_full': False})

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
@app.route('/user=/tv_show=<tv_show_id>/is_tv_show_in_slot', methods=['GET'])
@app.route('/user=<user_id>/tv_show=/is_tv_show_in_slot', methods=['GET'])
@app.route('/user=/tv_show=/is_tv_show_in_slot', methods=['GET'])
def is_tv_show_in_slot(user_id=None, tv_show_id=None):
    if UserSlots.query.filter_by(user_id=user_id).filter_by(tv_show_id=tv_show_id).scalar() is not None:
        return jsonify({'is_tv_show_in_slot': True})
    else:
        return jsonify({'is_tv_show_in_slot': False})


# { user_id: [user_id], tv_show_id: [tv_show_id] }
# creates a new slot in user_slots and adds tv show to that slot
@app.route('/add_tv_show', methods=['PUT'])
def add_tv_show(resub=False, new_slot_id=None, tv_show_id=None, user_id=None):
    # only run this section of code to add tv show to newly added slot
    try:
        if resub is False:
            data = request.get_json()
            user_id = data['user_id']
            tv_show_id = data['tv_show_id']

            # default boolean variables to success
            is_success = True
            is_valid_user = True
            is_valid_tv_show = True
            is_unique_tv_show = True

            current_user_tv_show_ids = list()
            if user_id is None or not isinstance(user_id, int) or user_id <= 0 or User.query.filter_by(
                    id=user_id).scalar() is None:
                is_success = False
                is_valid_user = False
                is_unique_tv_show = False
            if tv_show_id is None or not isinstance(tv_show_id, int) or tv_show_id <= 0:
                is_success = False
                is_valid_tv_show = False
                is_unique_tv_show = False
            if TVShows.query.filter_by(id=tv_show_id).scalar() is None:
                is_success = False
                is_valid_tv_show = False
            if is_valid_user is True:
                current_user_slots = UserSlots.query.filter_by(user_id=user_id).all()
                for slot in current_user_slots:
                    current_user_tv_show_ids.append(slot.tv_show_id)
                if tv_show_id in current_user_tv_show_ids:
                    is_success = False
                    is_unique_tv_show = False
            if is_success is False:
                return jsonify({'success': is_success,
                                'valid_user': is_valid_user,
                                'valid_tv_show': is_valid_tv_show,
                                'unique_tv_show': is_unique_tv_show})

        if resub is False:
            # Update user's slot number
            new_slot_id = increment_slot(user_id)
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
            user_slots.user_id = user_id,
            user_slots.slot_num = new_slot_id,
            user_slots.tv_show_id = tv_show_id,
            return 'success'

        return jsonify({'success': True,
                        'valid_user': True,
                        'valid_tv_show': True,
                        'unique_tv_show': True, })
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
        # casts input into int if string
        if user_id is None or tv_show_id is None:
            return jsonify({'is_success': False,
                            'is_slot_exist': False})
        if isinstance(user_id, str):
            if user_id.isdigit():
                user_id = int(user_id)
            else:
                return jsonify({'is_success': False,
                                'is_slot_exist': False})
        if isinstance(tv_show_id, str):
            if tv_show_id.isdigit():
                tv_show_id = int(tv_show_id)
            else:
                return jsonify({'is_success': False,
                                'is_slot_exist': False})

        if UserSlots.query.filter_by(user_id=user_id).filter_by(tv_show_id=tv_show_id).scalar() is not None:
            change_subscription_status(user_id, tv_show_id, False)
            db.session.commit()
            return jsonify({'is_success': True,
                            'is_slot_exist': True, })
        else:
            return jsonify({'is_success': False,
                            'is_slot_exist': False})
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
                            'is_slot_exist': False})
    except Exception as e:
        return str(e)


@app.route('/is_unsubscribed/user_id=<user_id>/tv_show_id=<tv_show_id>', methods=['GET'])
@app.route('/is_unsubscribed/user_id=/tv_show_id=<tv_show_id>', methods=['GET'])
@app.route('/is_unsubscribed/user_id=<user_id>/tv_show_id=', methods=['GET'])
@app.route('/is_unsubscribed/user_id=/tv_show_id=', methods=['GET'])
def is_unsubscribe(user_id=None, tv_show_id=None):
    unsubscribe_boolean = UserSlots.query.filter_by(user_id=user_id).filter_by(tv_show_id=tv_show_id).first()
    if unsubscribe_boolean is not None and unsubscribe_boolean.unsubscribe is True:
        return jsonify({"is_unsubscribed": True})
    return jsonify({"is_unsubscribed": False})


@app.route('/user=<user_id>/subscriptions', methods=['GET'])
@app.route('/user=/subscriptions', methods=['GET'])
def get_user_subscriptions(user_id=None):
    subscriptions = UserSlots.query.filter_by(user_id=user_id).all()
    subscriptions_id_list = list()
    for subscription in subscriptions:
        if subscription.tv_show_id is not None and subscription.unsubscribe is False:
            subscriptions_id_list.append(subscription.tv_show_id)
    subscription_obj_list = TVShows.query.filter(TVShows.id.in_(subscriptions_id_list)).all()
    return jsonify({'subscriptions': [subscription_obj.serialize() for subscription_obj in subscription_obj_list]})


# [url]//is_slot_deletable/user=[user_id]
@app.route('/is_slot_deletable/user=<user_id>', methods=['GET'])
@app.route('/is_slot_deletable/user=', methods=['GET'])
def is_slot_deletable(user_id=None):
    if user_id is not None and user_id.isdigit() and int(user_id) > 0:
        slots = UserSlots.query.filter_by(user_id=user_id).filter_by(delete_slot=False).all()
        slot_list = list()
        for slot in slots:
            slot_list.append(slot.tv_show_id)
        if len(slots) > 10:
            return jsonify({'valid_user_id': True,
                            'is_slot_deletable': True})
        return jsonify({'valid_user_id': True,
                        'is_slot_deletable': False})
    return jsonify({'valid_user_id': False,
                    'is_slot_deletable': False})


# { user_id: [user_id], slot_id: [slot_id] }
@app.route('/slot/flag/delete', methods=['PUT'])
def flag_slot_delete():
    try:
        data = request.get_json()
        user_id = data['user_id']
        slot_id = data['slot_id']

        if user_id is None or not isinstance(user_id, int):
            return jsonify({'valid_user_id': False,
                            'success': False})
        elif int(user_id) <= 0:
            return jsonify({'valid_user_id': False,
                            'success': False})

        user = User.query.filter_by(id=user_id).first()
        slot_to_flag = UserSlots.query.filter_by(user_id=user.id).filter_by(slot_num=slot_id).first()

        if slot_id is None or not isinstance(slot_id, int):
            return jsonify({'valid_user_id': True,
                            'success': False})
        elif not user.num_slots > 10 or int(slot_id) < 1:
            return jsonify({'valid_user_id': True,
                            'success': False})

        # Check Backwards
        for slot_num in range(user.num_slots, 10, -1):
            slot = UserSlots.query.filter_by(user_id=user.id).filter_by(slot_num=slot_num).first()

            if slot.delete_slot == 0:
                # Swap Unsubscribe Status
                temp_unsub_flag = slot_to_flag.unsubscribe
                slot_to_flag.unsubscribe = slot.unsubscribe
                slot.unsubscribe = temp_unsub_flag

                # Swap tv_show_ids
                temp_id = slot_to_flag.tv_show_id
                slot_to_flag.tv_show_id = slot.tv_show_id
                slot.tv_show_id = temp_id

                # Flag Slot
                slot.unsubscribe = 1
                slot.delete_slot = 1
                db.session.commit()
        return jsonify({'valid_user_id': True,
                        'success': True})
    except Exception as e:
        return str(e)


# [url]/server_update
@app.route('/database_update', methods=['DELETE'])
def database_update(func_call=False, user_id=None):
    try:
        if func_call is False:
            data = request.get_json()
            user_id = data['user_id']

        if user_id is not None and isinstance(user_id, int) and user_id > 0:
            user = User.query.filter_by(id=user_id).scalar()
            is_deletion_success = True
            if user is not None:
                # delete slots set to delete and check if slots can be deleted
                if delete_slots(user_id):
                    # set tv shows set for unsubscribe to null
                    delete_expired_tv_shows(user_id)
                    # remove expired rented movies
                    delete_expired_movies(user_id)
                    # email user
                    user.sub_date = datetime.now()
                    db.session.commit()
                    email_sender.subscription_renew_email(user.username, user.email, user.sub_date + timedelta(30))
                else:
                    if user.sub_date == (datetime.now() - timedelta(28)).date():
                        email_sender.sub_reminder_email(user.username, user.email)
                    is_deletion_success = False
                if not is_deletion_success:
                    return jsonify({'success': False,
                                    'valid_user_id': True,
                                    'deletions_success': is_deletion_success})

                return jsonify({'success': True,
                                'valid_user_id': True,
                                'deletions_success': is_deletion_success})
        return jsonify({'success': False,
                        'valid_user_id': False,
                        'deletions_success': False})
    except Exception as e:
        return str(e)


# [url]/search/user=[email_or_username]
@app.route('/search/user=<query>/page=<int:page>', methods=['GET'])
@app.route('/search/user=/page=<int:page>', methods=['GET'])
@app.route('/search/user=<query>', methods=['GET'])
@app.route('/search/user=', methods=['GET'])
def user_search(query=None, page=1):
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


# { request_to: [user_id], request_from: [pending_from_id] }
# send a friend request to another user
@app.route('/send_friend_request', methods=['POST'])
def send_friend_request():
    try:
        data = request.get_json()
        request_to = data['request_to']
        request_from = data['request_from']

        check_user_to = User.query.filter_by(id=request_to).scalar() is not None
        user_to = User.query.filter_by(id=request_to).first()
        check_user_from = User.query.filter_by(id=request_from).scalar() is not None
        user_from = User.query.filter_by(id=request_from).first()
        check_friendship = Friends.query.filter_by(user_id=request_from).filter_by(
            friend_id=request_to).scalar() is None
        if not isinstance(request_to, int):
            check_user_to = False
            check_friendship = False
        if not isinstance(request_from, int):
            check_user_from = False
            check_friendship = False

        if check_user_to and check_user_from and check_friendship:
            # add request to table
            new_friend_request = PendingFriends(
                user_id=request_to,
                pending_from_id=request_from,
            )
            db.session.add(new_friend_request)
            db.session.commit()
            email_sender.send_friend_request_notif_email(user_to.username, user_to.email, user_from.username)
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


# { user_id: [user_id], request_from: [pending_from_id] }
# accepts a friend request
@app.route('/accept_friend_request', methods=['POST'])
def accept_friend_request():
    try:
        data = request.get_json()
        user_id = data['user_id']
        pending_from_id = data['request_from']
        check_user_id = User.query.filter_by(id=user_id).first()
        check_user_id = check_user_id is not None
        check_friend_id = User.query.filter_by(id=pending_from_id).first()
        check_friend_id = check_friend_id is not None

        # checks for valid inputs
        if check_friend_id and check_user_id:
            check_friend_request = PendingFriends.query.filter_by(user_id=user_id).filter_by(
                pending_from_id=pending_from_id).first()
            check_friend_request = check_friend_request is not None
            # checks if friend request exists
            if check_friend_request:
                add_friend(user_id, pending_from_id)
                # delete request
                PendingFriends.query.filter_by(user_id=user_id).filter_by(pending_from_id=pending_from_id).delete()
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


# { user_id: [user_id], request_from: [pending_from_id] }
# decline a friend request
@app.route('/decline_friend_request', methods=['POST'])
def decline_friend_request():
    try:
        data = request.get_json()
        user_id = data['user_id']
        pending_from_id = data['request_from']
        check_user_id = User.query.filter_by(id=user_id).first()
        check_user_id = check_user_id is not None
        check_friend_id = User.query.filter_by(id=pending_from_id).first()
        check_friend_id = check_friend_id is not None

        # checks for valid inputs
        if check_friend_id and check_user_id:
            check_friend_request = PendingFriends.query.filter_by(user_id=user_id).filter_by(
                pending_from_id=pending_from_id).first()
            check_friend_request = check_friend_request is not None
            # checks if friend request exists
            if check_friend_request:
                # delete request
                PendingFriends.query.filter_by(user_id=user_id).filter_by(pending_from_id=pending_from_id).delete()
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


# returns true if user_id and friend_id is in the pending table
# [url]/has_friend_request/user_id=[user_id]/request_from=[pending_from_id]
@app.route('/has_friend_request/user_id=<user_id>/request_from=<request_from>', methods=['GET'])
@app.route('/has_friend_request/user_id=<user_id>/request_from=', methods=['GET'])
@app.route('/has_friend_request/user_id=/request_from=<request_from>', methods=['GET'])
@app.route('/has_friend_request/user_id=/request_from=', methods=['GET'])
def has_friend_request(user_id=None, request_from=None):
    if user_id is not None and request_from is not None and user_id.isdigit() and request_from.isdigit() and \
            int(user_id) > 0 and int(request_from) > 0:
        is_request = PendingFriends.query.filter_by(user_id=user_id).filter_by(pending_from_id=request_from).scalar()
        if is_request is not None:
            return jsonify({'has_friend_request': True})
    return jsonify({'has_friend_request': False})


# returns a list of all friend requests from a specific user
# [url]/get_friend_requests/user=[user_id]
@app.route('/get_friend_requests/user=<user_id>', methods=['GET'])
@app.route('/get_friend_requests/user=<user_id>/page=<int:page>', methods=['GET'])
@app.route('/get_friend_requests/user=/page=', methods=['GET'])
@app.route('/get_friend_requests/user=', methods=['GET'])
def get_friend_requests(user_id=None, page=1):
    pending_friend_list = list()
    if user_id is not None and user_id.isdigit() and int(user_id) > 0:
        pending_request_rel = PendingFriends.query.filter_by(user_id=user_id).all()
        for request in pending_request_rel:
            pending_friend = User.query.filter_by(id=request.pending_from_id).first()
            pending_friend_list.append(pending_friend)
    return paginated_json('pending_friend_requests', pending_friend_list, page)


# checks if there is at least 1 pending friend request and returns True if there is
# [url]/is_friend_request/user=[user_id]
@app.route('/is_friend_request/user=<user_id>', methods=['GET'])
@app.route('/is_friend_request/user=', methods=['GET'])
def is_friend_request(user_id=None):
    friend_request_boolean = False
    if user_id is not None and user_id.isdigit() and int(user_id) > 0:
        friend_request_boolean = PendingFriends.query.filter_by(user_id=user_id).scalar() is not None
    return jsonify({'at_least_one_request': friend_request_boolean})


# Check Friendship
# [url]/user1=[user1_id]/user2=[user2_id]
@app.route('/user1=<user1_id>/user2=<user2_id>', methods=['GET'])
@app.route('/user1=<user1_id>/user2=', methods=['GET'])
@app.route('/user1=/user2=<user2_id>', methods=['GET'])
@app.route('/user1=/user2=', methods=['GET'])
def is_friend(user1_id=None, user2_id=None, func_call=False):
    if user1_id is None or user1_id is '' or user2_id is None or user2_id is '':
        return jsonify({'is_friend': False})

    user1_id = '{}%'.format(user1_id)
    user2_id = '{}%'.format(user2_id)

    friendship = Friends.query.filter_by(user_id=user1_id).filter_by(friend_id=user2_id).first()
    if friendship is not None:
        if func_call:
            return True
        return jsonify({'is_friend': True})
    else:
        if func_call:
            return False
        return jsonify({'is_friend': False})


# Display user friends
# [url]/users=[user_id]/friends/page=[page]
# [url]/users=[user_id]/friends
@app.route('/user=<user_id>/friends/page=<int:page>', methods=['GET'])
@app.route('/user=<user_id>/friends/page=', methods=['GET'])
@app.route('/user=<user_id>/friends', methods=['GET'])
@app.route('/user=/friends', methods=['GET'])
def get_user_friend_list(user_id=None, page=1):
    friend_list = list()

    if user_id is None or not user_id.isdigit():
        return paginated_json('friends', friend_list, page)

    # Ensure Valid User ID
    user = User.query.filter_by(id=user_id).first()
    if user is not None:
        # Get list of all entries with the User's ID
        friends = Friends.query.filter_by(user_id=user_id)

        # Create list of the user's friend's IDs
        friend_ids = list()
        for friend in friends:
            if friend.friend_id != int(user_id):
                friend_ids.append(friend.friend_id)

        # Append the Users that match the friend IDs
        for friend_id in friend_ids:
            friend_list.append(User.query.filter_by(id=friend_id).first())

    return paginated_json('friends', friend_list, page)


# [url]/user=[user_id]/friends/remove=[friend_id]
@app.route('/user=<user_id>/friends/remove=<friend_id>', methods=['DELETE'])
@app.route('/user=<user_id>/friends/remove=', methods=['DELETE'])
@app.route('/user=/friends/remove=<friend_id>', methods=['DELETE'])
@app.route('/user=/friends/remove=', methods=['DELETE'])
def remove_friend(user_id=None, friend_id=None):
    if (user_id is None or not user_id.isdigit()) and (friend_id is None or not friend_id.isdigit()):
        return jsonify({'user_exist': False, 'friend_exist': False, 'friend_deleted': False})

    user = User.query.filter_by(id=user_id).first()
    friend = User.query.filter_by(id=friend_id).first()

    if user is None and friend is None:
        return jsonify({'user_exist': False, 'friend_exist': False, 'friend_deleted': False})
    elif friend is None:
        return jsonify({'user_exist': True, 'friend_exist': False, 'friend_deleted': False})
    elif user is None:
        return jsonify({'user_exist': False, 'friend_exist': True, 'friend_deleted': False})
    else:
        relationship = Friends.query.filter_by(user_id=user_id).filter_by(friend_id=friend_id).first()

        if relationship is None or user_id == friend_id:
            return jsonify({'user_exist': True, 'friend_exist': False, 'friend_deleted': False})
        else:
            Friends.query.filter_by(user_id=user_id).filter_by(friend_id=friend_id).delete()
            Friends.query.filter_by(user_id=friend_id).filter_by(friend_id=user_id).delete()
            db.session.commit()
            return jsonify({'user_exist': True, 'friend_exist': True, 'friend_deleted': True})


# Display user's slots
# [url]/user=[user_id]/slots
@app.route('/user=<user_id>/slots', methods=['GET'])
@app.route('/user=/slots', methods=['GET'])
def get_user_slots(user_id=None):
    if user_id is None or not user_id.isdigit():
        return jsonify({'user_slots': list()})

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
    else:
        return jsonify({'user_slots': list()})


# [url]/users=[user_id]/movie_list
@app.route('/user=<user_id>/movie_list', methods=['GET'])
@app.route('/user=/movie_list', methods=['GET'])
def get_user_movie_list(user_id=None):
    user_rated_movies = list()

    if user_id is None or not user_id.isdigit():
        return jsonify({'movie_list': user_rated_movies})

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

            if rating is None:
                rating = 0

            rm = RatedMovie(movie_id, title, image_url, rating)
            rated_movies.append(rm)

        user_rated_movies = DisplayRatedMovie(user.id, rated_movies)
        return jsonify({'movie_list': user_rated_movies.serialize()})
    else:
        return jsonify({'movie_list': user_rated_movies})


# [url]/user=[user_id]/movie=[movie_id]/rating
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


# { user_id: [user_id], movie_id: [movie_id], rating: [1-5] }
@app.route('/user=<user_id>/movie=<movie_id>/rating', methods=['GET'])
@app.route('/user=/movie=<movie_id>/rating', methods=['GET'])
@app.route('/user=<user_id>/movie=/rating', methods=['GET'])
@app.route('/user=/movie=/rating', methods=['GET'])
def get_user_movie_rating(user_id=None, movie_id=None):
    if user_id is None or not user_id.isdigit() or movie_id is None or not movie_id.isdigit():
        return jsonify({'movie_rating': None})

    else:
        entry = UserRatedMovieRel.query.filter_by(user_id=user_id).filter_by(movie_id=movie_id).first()
        if entry is None:
            return jsonify({'movie_rating': 0})

        return jsonify({'movie_rating': entry.user_rating})


# [url]/rate/movie
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
@app.route('/movie=/comments', methods=['GET'])
def get_movie_comments(title=None, reverse=False):
    if title is None:
        return jsonify({'valid_movie': False})

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


# [url]/user=[user_id]/tv_show_list
@app.route('/user=<user_id>/tv_show_list', methods=['GET'])
@app.route('/user=/tv_show_list', methods=['GET'])
def get_user_tv_show_list(user_id=None):
    user_rated_tv_shows = list()

    if user_id is None or not user_id.isdigit():
        return jsonify({'tv_show_list': user_rated_tv_shows})

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
    else:
        return jsonify({'tv_show_list': user_rated_tv_shows})


# [url]/user=[user_id]/tv_show=[tv_show_id]/rating
@app.route('/user=<user_id>/tv_show=<tv_show_id>/rating', methods=['GET'])
@app.route('/user=<user_id>/tv_show=/rating', methods=['GET'])
@app.route('/user=/tv_show=<tv_show_id>/rating', methods=['GET'])
@app.route('/user=/tv_show=/rating', methods=['GET'])
def get_user_tv_show_rating(user_id=None, tv_show_id=None):
    if user_id is None or not user_id.isdigit() or tv_show_id is None or not tv_show_id.isdigit():
        return jsonify({'tv_show_rating': None})

    else:
        entry = UserRatedTVShowRel.query.filter_by(user_id=user_id).filter_by(tv_show_id=tv_show_id).first()
        return jsonify({'tv_show_rating': entry.user_rating})


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
@app.route('/tv_show=/comments', methods=['GET'])
def get_tv_show_comments(title=None, reverse=False):
    if title is None:
        return jsonify({'valid_tv_show': False})

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


# [url]/user=[user_id]/movie=[movie_id]/is_movie_rented
@app.route('/user=<user_id>/movie=<movie_id>/is_movie_rented', methods=['GET'])
@app.route('/user=<user_id>/movie=/is_movie_rented', methods=['GET'])
@app.route('/user=/movie=<movie_id>/is_movie_rented', methods=['GET'])
@app.route('/user=/movie=/is_movie_rented', methods=['GET'])
def is_movie_rented(user_id=None, movie_id=None):
    if UserRentedMovies.query.filter_by(user_id=user_id).filter_by(movie_id=movie_id).first() is not None:
        return jsonify({'is_movie_rented': True})
    else:
        return jsonify({'is_movie_rented': False})


@app.route('/user=<user_id>/rented_movies', methods=['GET'])
@app.route('/user=/rented_movies', methods=['GET'])
def get_user_rented_movies(user_id=None):
    movies = list()

    if user_id is None or user_id is '' or not user_id.isdigit():
        return jsonify({'user_rented_movies': movies})

    if User.query.filter_by(id=user_id).first() is not None:
        user_movie_rel = UserRentedMovies.query.filter_by(user_id=user_id).all()
        for user_movie in user_movie_rel:
            movies.append(Movie.query.filter_by(id=user_movie.movie_id).first())

        return jsonify({'user_rented_movies': [movie.serialize() for movie in movies]})
    else:
        return jsonify({'user_rented_movies': movies})


# { user_id: [user_id], movie_id: [movie_id] }
# adds rented movie into user_rented_movies table
@app.route('/rent_movie', methods=['POST'])
def rent_movie():
    try:
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

        user_rented_movies = UserRentedMovies(
            user_id=user_id,
            movie_id=movie_id,
            rent_datetime=rent_datetime
        )
        db.session.add(user_rented_movies)
        db.session.commit()

        email_sender.movie_email(user_check.username, user_check.email, movie_check.title)
        return jsonify({'success': True,
                        'valid_user': True,
                        'valid_movie': True})
    except Exception as e:
        return str(e)


# { "user_id": [user_id], "post_user_id": [post_user_id], "post": [post_text] }
# [url]/timeline/post
@app.route('/timeline/post', methods=['POST'])
def post_timeline():
    try:
        data = request.get_json()
        wall_id = data['wall_id']
        user_id = data['user_id']
        post = data['post']
        date_of_post = datetime.now()

        if User.query.filter_by(id=wall_id).first() is None:
            return jsonify({'success': False,
                            'valid_user': False,
                            'valid_friend': False})

        # Can only post if friend
        if is_friend(user_id, wall_id, True):
            timeline = TimeLine(wall_id=wall_id,
                                user_id=user_id,
                                post=post,
                                date_of_post=date_of_post)
            db.session.add(timeline)
            db.session.commit()

            return jsonify({'success': True,
                            'valid_user': True,
                            'valid_friend': True,
                            'post_id': timeline.post_id})
        else:
            return jsonify({'success': False,
                            'valid_user': True,
                            'valid_friend': False})
    except Exception as e:
        return str(e)


# { "post_id": [post_id], "user_id": [user_id], "comment": [comment_text] }
# [url]/timeline/post/comment
@app.route('/timeline/post/comment', methods=['POST'])
def comment_on_post():
    try:
        data = request.get_json()
        post_id = data['post_id']
        user_id = data['user_id']
        comment = data['comment']
        date_of_comment = datetime.now()

        if User.query.filter_by(id=user_id).first() is None:
            return jsonify({'success': False,
                            'valid_user': False,
                            'valid_friend': False,
                            'valid_post_id': False})

        elif TimeLine.query.filter_by(post_id=post_id).first() is None:
            return jsonify({'success': False,
                            'valid_user': True,
                            'valid_friend': False,
                            'valid_post_id': False})

        wall_id = TimeLine.query.filter_by(post_id=post_id).first().wall_id
        post_user_id = TimeLine.query.filter_by(post_id=post_id).first().user_id
        # Can only post if friend
        if is_friend(user_id, wall_id, True):

            post_comment = PostComments(wall_id=wall_id,
                                        post_user_id=post_user_id,
                                        user_id=user_id,
                                        comment=comment,
                                        date_of_comment=date_of_comment,
                                        post_id=post_id)
            db.session.add(post_comment)
            db.session.commit()

            return jsonify({'success': True,
                            'valid_user': True,
                            'valid_friend': True,
                            'valid_post_id': True,
                            'comment_id': post_comment.comment_id})
        else:
            return jsonify({'success': False,
                            'valid_user': True,
                            'valid_friend': False,
                            'valid_post_id': True})

    except Exception as e:
        return str(e)


# [url]/user=[user_id]/wall
@app.route('/user=<user_id>/wall', methods=['GET'])
@app.route('/user=/wall', methods=['GET'])
def display_wall(user_id=None):
    wall = list()

    if user_id is None or user_id is '' or not user_id.isdigit():
        return jsonify({'wall': wall})

    user = User.query.filter_by(id=user_id).first()

    if user is not None:
        wall_posts = TimeLine.query.filter_by(wall_id=user.id).order_by(TimeLine.date_of_post)

        for post in wall_posts:
            user = User.query.filter_by(id=post.wall_id).first()
            post_user = User.query.filter_by(id=post.user_id).first()

            comments = list()
            comment_list = PostComments.query.filter_by(user_id=post.wall_id).filter_by(
                post_user_id=post_user.id).filter_by(post_id=post.post_id)
            for comment in comment_list:
                comment_user = User.query.filter_by(id=comment.user_id).first()
                comments.append(PostComment(
                    user_id=user.id,
                    username=user.username,
                    post_user_id=post_user.id,
                    post_username=post_user.username,
                    comment_user_id=comment_user.id,
                    comment_username=comment_user.username,
                    comment=comment.comment,
                    date_of_comment=comment.date_of_comment,
                ))

            wall.append(Post(
                post_id=post.post_id,
                user_id=user.id,
                username=user.username,
                post_user_id=post_user.id,
                post_username=post_user.username,
                post=post.post,
                date_of_post=post.date_of_post,
                comments=reversed(comments),
            ))
        wall.sort(key=lambda w: w.date_of_post)
        wall = reversed(wall)

        return jsonify({'wall': [w.serialize() for w in wall]})
    else:
        return jsonify({'wall': wall})


# [url]/user=[user_id]/timeline
@app.route('/user=<user_id>/timeline', methods=['GET'])
@app.route('/user=/timeline', methods=['GET'])
def display_timeline(user_id=None):
    timeline = list()

    if user_id is None or user_id is '' or not user_id.isdigit():
        return jsonify({'timeline': timeline})

    user = User.query.filter_by(id=user_id).first()

    if user is not None:
        friend_list = Friends.query.filter_by(user_id=user.id)

        # View All Self and Friend Walls
        for friend in friend_list:
            friend_wall = TimeLine.query.filter_by(wall_id=friend.friend_id).order_by(TimeLine.date_of_post)

            for post in friend_wall:
                user = User.query.filter_by(id=post.wall_id).first()
                post_user = User.query.filter_by(id=post.user_id).first()

                comments = list()
                comment_list = PostComments.query.filter_by(user_id=post.wall_id).filter_by(
                    post_user_id=post.user_id).filter_by(post_id=post.post_id)
                for comment in comment_list:
                    comment_user = User.query.filter_by(id=comment.user_id).first()
                    comments.append(PostComment(
                        user_id=user.id,
                        username=user.username,
                        post_user_id=post_user.id,
                        post_username=post_user.username,
                        comment_user_id=comment_user.id,
                        comment_username=comment_user.username,
                        comment=comment.comment,
                        date_of_comment=comment.date_of_comment,
                    ))

                timeline.append(Post(
                    post_id=post.post_id,
                    user_id=user.id,
                    username=user.username,
                    post_user_id=post_user.id,
                    post_username=post_user.username,
                    post=post.post,
                    date_of_post=post.date_of_post,
                    comments=reversed(comments),
                ))

        timeline.sort(key=lambda tl: tl.date_of_post)
        timeline = reversed(timeline)

        return jsonify({'timeline': [tl.serialize() for tl in timeline]})
    else:
        return jsonify({'timeline': timeline})


# add friend friend and friend adds back
def add_friend(user_id, friend_id):
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


def update_average_rating(is_tv_show: bool, media_id: int):
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


def get_average_rating(is_tv_show: bool, media_id: int):
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


# checks database if movies are past rented due date and deletes them
def delete_expired_movies(user_id=None):
    yesterday_datetime = datetime.now() - timedelta(1)
    check_not_none = UserRentedMovies.query.filter_by(user_id=user_id).filter(
        UserRentedMovies.rent_datetime <= yesterday_datetime).scalar() is not None
    if check_not_none:
        rented_movies = UserRentedMovies.query.filter_by(user_id=user_id).filter(
            UserRentedMovies.rent_datetime <= yesterday_datetime).all()
        user = User.query.filter_by(id=user_id).first()

        for movie in rented_movies:
            # Get movie title
            movie_obj = Movie.query.filter_by(id=movie.movie_id).first()
            email_sender.movie_return_email(user.username, user.email, movie_obj.title)

        UserRentedMovies.query.filter_by(user_id=user_id).filter(
            UserRentedMovies.rent_datetime <= yesterday_datetime).delete()


# { user_id: [user_id] }
def delete_slots(user_id=None):
    user = User.query.filter_by(id=user_id).first()

    if user is None or user.sub_date >= (datetime.now() - timedelta(30)).date():
        return False

    # Check Backwards
    for slot_num in range(user.num_slots, 10, -1):
        slot = UserSlots.query.filter_by(user_id=user.id).filter_by(slot_num=slot_num).first()

        if slot.delete_slot == 1:
            UserSlots.query.filter_by(user_id=user.id).filter_by(slot_num=slot_num).delete()
            user.num_slots -= 1

    return True


# need to add to login function and need to add check to not allow deleting slots past 10
def delete_expired_tv_shows(user_id=None):
    month_ago_date = (datetime.now() - timedelta(30)).date()
    expired_user = User.query.filter_by(id=user_id).filter(User.sub_date <= month_ago_date).scalar()
    if expired_user is not None:
        tv_show_to_remove_list = UserSlots.query.filter_by(user_id=user_id).filter_by(unsubscribe=True)
        for tv_show_to_remove in tv_show_to_remove_list:
            subscribe(user_id, tv_show_to_remove.tv_show_id, True)
            remove_tv_show(user_id, tv_show_to_remove.tv_show_id)
    return True


# function to delete tv_show in slot
def remove_tv_show(user_id=None, tv_show_id=None):
    # get slot_num of deleted tv show
    deletion_index = UserSlots.query.filter_by(user_id=user_id).filter_by(tv_show_id=tv_show_id).first()
    deletion_index.tv_show_id = None


# (Pseudo PUT) increment user's slot_num by 1 and return new slot_id
def increment_slot(user_id) -> int:
    # increment slot number in users
    user = User.query.filter_by(id=user_id).first()
    user.num_slots = user.num_slots + 1

    return user.num_slots


def change_subscription_status(user_id, tv_show_id, unsubscribe_boolean):
    # increment slot number in users
    user_slot = UserSlots.query.filter_by(user_id=user_id).filter_by(tv_show_id=tv_show_id).first()

    user_slot.user_id = user_id
    user_slot.slot_num = user_slot.slot_num
    user_slot.tv_show_id = tv_show_id
    user_slot.unsubscribe = unsubscribe_boolean


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
