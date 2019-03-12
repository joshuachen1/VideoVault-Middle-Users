from app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR)
    email = db.Column(db.VARCHAR)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
        }


class Friends(db.Model):
    __tablename__ = 'user_friend_list'

    user_id = db.Column(db.Integer, primary_key=True)
    friend_id = db.Column(db.Integer, primary_key=True)

    def __init__(self, user_id, friend_id):
        self.user_id = user_id
        self.friend_id = friend_id

    def __repr__(self):
        return '<user_id {} friend_id {}>'.format(self.user_id, self.friend_id)

    def serialize(self):
        return {
            'user_id': self.user_id,
            'friend_id': self.friend_id,
        }


class UserRatedMovieRel(db.Model):
    __tablename__ = 'user_rated_movies'

    user_id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, primary_key=True)
    user_rating = db.Column(db.Integer)

    def __init__(self, user_id, movie_id, user_rating):
        self.user_id = user_id
        self.movie_id = movie_id
        self.user_rating = user_rating

    def __repr__(self):
        return '<user_id {} movie_id {} user_rating {}'.format(self.user_id, self.movie_id, self.user_rating)

    def serialize(self):
        return {
            'user_id': self.user_id,
            'movie_id': self.movie_id,
            'rating': self.user_rating,
        }


class UserRatedTVShowRel(db.Model):
    __tablename__ = 'user_rated_tv_shows'

    user_id = db.Column(db.Integer, primary_key=True)
    tv_show_id = db.Column(db.Integer, primary_key=True)
    user_rating = db.Column(db.Integer)

    def __init__(self, user_id, tv_show_id, user_rating):
        self.user_id = user_id
        self.tv_show_id = tv_show_id
        self.user_rating = user_rating

    def __repr__(self):
        return '<user_id {} tv_show_id {} user_rating {}'.format(self.user_id, self.tv_show_id, self.user_rating)

    def serialize(self):
        return {
            'user_id': self.user_id,
            'tv_show_id': self.tv_show_id,
            'rating': self.user_rating,
        }

