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
from user_media_models import Movie, MovieComment, TVShows, TVShowComment

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

# [url]/add_slot
@app.route('/add_slot', methods=['PUT'])
def add_slot():
    # increment slot number in users
    data = request.get_json()
    user_id = data['id']
    name = str(data['name'])
    username = str(data['username'])
    email = str(data['email'])
    password = str(data['password'])
    card_num = str(data['card_num'])
    num_slots = data['num_slots']
    sub_date = data['sub_date']

    check_id = User.query.filter_by(id=user_id).first()
    check_num_slots = check_id.num_slots + 1

    if check_id is None and num_slots != check_num_slots:
        return jsonify({'success':False,
                        'valid_user':False,
                        'valid_num_slots':False})
    elif check_id is None:
        return jsonify({'success': False,
                        'valid_user': False,
                        'valid_num_slots': True})
    elif num_slots != check_num_slots:
        return jsonify({'success': False,
                        'valid_user': True,
                        'valid_num_slots': False})

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
        db.session.commit()

        # Add a new entry to user_slot
        add_empty_slot(user_id, num_slots)

        return jsonify({'success':True,
                        'valid_user':True,
                        'valid_num_slots':True})
    except Exception as e:
        return str(e)


@app.route('/resub', methods=['PUT'])
def resub():
    data = request.get_json()
    user_id = data['user_id']
    tv_show_id = str(data['tv_show_id'])

    tv_show_ids = [id.strip() for id in tv_show_id.split(',')]
    user_check = User.query.filter_by(id=user_id).first()
    tv_show_len = len(set(tv_show_id))

    # add each entry to the user_slots table
    i = 1
    for tv_show_id in tv_show_ids:
        tv_show_check = TVShows.query.filter_by(id=tv_show_id).first()

        # return boolean for invalid inputs
        if user_check is None and (tv_show_check is None or tv_show_len is not 10):
            return jsonify({'success:': False,
                            'valid_user': False,
                            'valid_tv_shows': False})
        elif user_check is None:
            return jsonify({'success:': False,
                            'valid_user': False,
                            'valid_tv_shows': True})
        elif tv_show_check is None or tv_show_len is not 10:
            return jsonify({'success': False,
                            'valid_user': True,
                            'valid_tv_shows': False})

        slot_num = i
        add_tv_show(True, slot_num, tv_show_id, user_id)
        i = i + 1

    db.session.commit()
    return jsonify({'success:':True,
                    'valid_user':True,
                    'valid_tv_shows':True})


# Json input: user_id, slot_num, tv_show_title
@app.route('/add_tv_show', methods=['PUT'])
def add_tv_show(resub=False, slot_num=None, tv_show_id=None, user_id=None):
    # only run this section of code to add tv show to newly added slot
    if resub is False:
        data = request.get_json()
        user_id = data['user_id']
        slot_num = data['slot_num']
        tv_show_id = data['tv_show_id']

        user_check = User.query.filter_by(id=user_id).first()
        tv_show_list = UserSlots.query.filter_by(user_id=user_id).all()
        tv_show_check = TVShows.query.filter_by(id=tv_show_id).first()

        tv_show_id_list = list()
        for slot in tv_show_list:
            tv_show_id_list.append(slot.tv_show_id)

        # checks to see if input is valid
        if user_check is None and (tv_show_check is None or tv_show_id in tv_show_id_list):
            return jsonify({'success:': False,
                            'valid_user': False,
                            'valid_tv_show': False})
        elif user_check is None:
            return jsonify({'success:': False,
                            'valid_user': False,
                            'valid_tv_show': True})
        elif tv_show_check is None or tv_show_id in tv_show_id_list:
            return jsonify({'success': False,
                            'valid_user': True,
                            'valid_tv_show': False})

    try:
        # adds tv show to slot
        user = UserSlots.query.filter_by(slot_num=slot_num).filter_by(user_id=user_id).first()
        user.user_id = user_id
        user.slot_num = slot_num
        user.tv_show_id = tv_show_id

        if resub is False:
            db.session.commit()
        return jsonify({'success':True,
                        'valid_user':True,
                        'valid_tv_show':True})
    except Exception as e:
        return str(e)


# [url]/search/user=[email_or_username]
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


# Check Friendship
# [url]/user1=[user1_id]/user2=[user2_id]
@app.route('/user1=<int:user1_id>/user2=<int:user2_id>')
def is_friend(user1_id=None, user2_id=None):
    try:
        friendship = Friends.query.filter_by(user_id=user1_id).filter_by(friend_id=user2_id).first()
        if friendship is not None:
            return jsonify({'is_friend': True})
        else:
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
        date_of_comment = str(date.today())

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


@app.route('/tv_show/comment', methods=['POST'])
def comment_tv_show():
    try:
        data = request.get_json()
        tv_show_id = data['tv_show_id']
        user_id = data['user_id']
        comment = data['comment']
        date_of_comment = str(date.today())

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
def get_user_rented_movies(user_id=None):
    try:
        movies = list()
        user_movie_rel = UserRentedMovies.query.filter_by(user_id=user_id).all()
        for user_movie in user_movie_rel:
            movies.append(Movie.query.filter_by(id=user_movie.movie_id).first())

        return jsonify({'user_rented_movies': [movie.serialize() for movie in movies]})

    except Exception as e:
        return str(e)


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
        return jsonify({'success':False,
                        'valid_user':False,
                        'valid_movie':False})
    elif user_check is None:
        return jsonify({'success':False,
                        'valid_user':False,
                        'valid_movie':True})
    elif movie_check is None:
        return jsonify({'success':True,
                        'valid_user':True,
                        'valid_movie':False})

    try:
        user_rented_movies = UserRentedMovies(
            user_id=user_id,
            movie_id=movie_id,
            rent_datetime=rent_datetime
        )
        db.session.add(user_rented_movies)
        db.session.commit()
        return jsonify({'success':True,
                        'valid_user':True,
                        'valid_movie':True})
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

            return total / num_ratings

        else:
            movie_ratings = UserRatedMovieRel.query.filter_by(movie_id=media_id)
            total = 0
            num_ratings = 0

            for mr in movie_ratings:
                total += mr.user_rating
                num_ratings += 1

            return total / num_ratings

    except Exception as e:
        return str(e)


# adds an empty slot to user_slots in database
def add_empty_slot(user_id, slot_num):
    user_slots = UserSlots(
        user_id=user_id,
        slot_num=slot_num,
        tv_show_id=None
    )
    db.session.add(user_slots)
    db.session.commit()
    return "user_slots added"


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
