from cryptography.fernet import Fernet
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import date, datetime
import pymysql
import math
import os

# Setup App
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])  # Should change based on is in Development or Production
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS
CORS(app)

# Start Database
db = SQLAlchemy(app)

# Enable Variable Port for Heroku
port = int(os.environ.get('PORT', 33507))

# Import Models
from crypto_models import Key
from user_models import Signup, Login
from user_models import User, Friends
from user_models import Slot, UserSlots, DisplayUserSlots, UserRentedMovies
from user_models import UserRatedMovieRel, DisplayRatedMovie, RatedMovie
from user_models import UserRatedTVShowRel, DisplayRatedTVShow, RatedTVShow
from user_media_models import Movie, TVShows, UserRatedMedia

# Force pymysql to be used as replacement for MySQLdb
pymysql.install_as_MySQLdb()


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
            return jsonify(user_info.serialize())
        else:
            result = Login(False, True, False)
            return jsonify(result.serialize())
    except Exception as e:
        return str(e)


# [url]/signup
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
                sub_date=sub_date
            )
            db.session.add(user)

            new_user = User.query.filter_by(username=username).first()
            for i in range(num_slots):
                slot = UserSlots(
                    user_id=new_user.id,
                    slot_num=(i + 1),
                    tv_show_id=None,
                )
                db.session.add(slot)

            db.session.commit()

            return jsonify(new_user.serialize())
        except Exception as e:
            return str(e)
    except Exception as e:
        return str(e)


@app.route('/add_slot', methods=['PUT'])
def add_slot():
    data = request.get_json()
    newId = data['id']
    name = str(data['name'])
    username = str(data['username'])
    email = str(data['email'])
    password = str(data['password'])
    card_num = str(data['card_num'])
    num_slots = data['num_slots']
    sub_date = data['sub_date']
    try:
        user = User.query.filter_by(id=newId).first()
        if newId is not None:
            user.id = newId
        user.name = name
        user.username = username
        user.email = email
        user.password = password
        user.card_num = card_num
        user.num_slots = num_slots
        user.sub_date = sub_date
        db.session.commit()

        add_empty_slot(newId, num_slots)

        return "1 slot added"
    except Exception as e:
        return str(e)


@app.route('/resub', methods=['PUT'])
def resub():
    data = request.get_json()
    user_id = data['user_id']
    tv_show_id = str(data['tv_show_id'])

    tv_show_ids = [id.strip() for id in tv_show_id.split(',')]

    i = 1
    for tv_show_id in tv_show_ids:
        slot_num = i
        add_tv_show(True, slot_num, tv_show_id, user_id)
        i = i + 1
    return 'success'


# Json input: user_id, slot_num, tv_show_title
@app.route('/add_tv_show', methods=['PUT'])
def add_tv_show(resub=False, slot_num=None, tv_show_id=None, user_id=None):
    if resub is False:
        data = request.get_json()
        user_id = data['user_id']
        slot_num = data['slot_num']
        tv_show_id = data['tv_show_id']

    try:
        user=UserSlots.query.filter_by(slot_num=slot_num).filter_by(user_id=user_id).first()
        user.user_id = user_id
        user.slot_num = slot_num
        user.tv_show_id = tv_show_id

        db.session.commit()
        return "tv show added"
    except Exception as e:
        return str(e)


@app.route('/search/user=<query>', methods=['GET'])
@app.route('/search/user=', methods=['GET'])
def user_search(query=None):
    try:
        # Assume query == username
        if User.query.filter_by(email=query).first() is not None:
            user = User.query.filter_by(email=query).first()
            return jsonify({user.username: user.serialize()})

        # Assume query == username
        elif User.query.filter_by(username=query).first() is not None:
            user = User.query.filter_by(username=query).first()
            return jsonify({user.username: user.serialize()})

        else:
            return jsonify({'user_exist': False})

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
                friend_ids.append(friend.friend_id)

            # Append the Users that match the friend IDs
            for friend_id in friend_ids:
                friend_list.append(User.query.filter_by(id=friend_id).first())

        return paginated_json('friends', friend_list, page)

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
                    slot = Slot(user_slot.slot_num, None)
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


@app.route('/user=<int:user_id>/rented_movies', methods=['GET'])
def get_user_rented_movies(user_id = None):
    try:
        movies = list()
        user_movie_rel = UserRentedMovies.query.filter_by(user_id = user_id).all()
        for user_movie in user_movie_rel:
            movies.append(Movie.query.filter_by(id = user_movie.movie_id).first())

        return jsonify({'user_rented_movies': [movie.serialize() for movie in movies]})

    except Exception as e:
        return str(e)


@app.route('/rent_movie', methods=['POST'])
def rent_movie():
    data = request.get_json()
    user_id = data['user_id']
    movie_id = data['movie_id']
    rent_datetime = datetime.now()

    try:
        user_rented_movies = UserRentedMovies(
            user_id = user_id,
            movie_id = movie_id,
            rent_datetime = rent_datetime
        )
        db.session.add(user_rented_movies)
        db.session.commit()
        return 'movie rental success'
    except Exception as e:
        return str(e)


def add_empty_slot(user_id, slot_num):
    user_slots = UserSlots(
        user_id=user_id,
        slot_num=slot_num,
        tv_show_id=None
    )
    db.session.add(user_slots)
    db.session.commit()
    return "user_slots added"


def tv_show_to_id(title):
    tv_show = TVShows.query.filter_by(title=title).first()
    return tv_show.id


# Pseudo Pagination
def pseudo_paginate(page: int, list_to_paginate: []):
    start_page = (page - 1) * app.config['POSTS_PER_PAGE']
    end_page = start_page + app.config['POSTS_PER_PAGE']
    if end_page > len(list_to_paginate):
        end_page = len(list_to_paginate)

    return list_to_paginate[start_page:end_page]


# Return json
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
