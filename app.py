from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
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
from user_models import User, Friends
from user_models import RatedMovies
from user_media_models import Movie

# Force pymysql to be used as replacement for MySQLdb
pymysql.install_as_MySQLdb()


# [url]/
@app.route('/')
def hello_world():
    return 'Home Page'


# [url]/users/page=[page]
# [url]/users
@app.route('/users/page=<int:page>')
@app.route('/users/page=')
@app.route('/users')
def get_users(page=1):
    try:
        users = User.query.order_by().all()
        return paginated_json('users', users, page)
    except Exception as e:
        return str(e)


# [url]/users=[user_id]/friends/page=[page]
# [url]/users=[user_id]/friends
@app.route('/user=<int:user_id>/friends/page=<int:page>')
@app.route('/user=<int:user_id>/friends/page=')
@app.route('/user=<int:user_id>/friends')
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


# [url]/users=[user_id]/movie_list/page=[page]
# [url]/users=[user_id]/movie_list
@app.route('/user=<int:user_id>/movie_list/page=<int:page>')
@app.route('/user=<int:user_id>/movie_list/page=')
@app.route('/user=<int:user_id>/movie_list')
def get_user_movie_list(user_id=None, page=1):
    try:
        movie_list = list()

        # Ensure Valid User ID
        user = User.query.filter_by(id=user_id).first()
        if user is not None:
            # Get list of all entries with the User's ID
            rated_movies = RatedMovies.query.filter_by(user_id=user_id)

            # Create list of the user's rated movie's IDs
            movie_ids = list()
            for movie in rated_movies:
                movie_ids.append(movie.movie_id)

            # Append the Movies that match the Movie IDs
            for movie_id in movie_ids:
                movie_list.append(Movie.query.filter_by(id=movie_id).first())

        return paginated_json('movie_list', movie_list, page)

    except Exception as e:
        return str(e)


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
