from app import db


class Signup:
    def __init__(self, email_taken: bool, username_taken: bool, signup_successful: bool):
        self.email_taken = email_taken
        self.username_taken = username_taken
        self.signup_successful = signup_successful

    def serialize(self):
        return {
            'email_taken': self.email_taken,
            'username_taken': self.username_taken,
            'signup_successful': self.signup_successful,
        }


class Login:
    def __init__(self, invalid_email: bool, invalid_password: bool, login_successful: bool):
        self.invalid_email = invalid_email
        self.invalid_password = invalid_password
        self.login_successful = login_successful

    def serialize(self):
        return {
            'invalid_email': self.invalid_email,
            'invalid_password': self.invalid_password,
            'login_successful': self.login_successful,
        }


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR)
    username = db.Column(db.VARCHAR, unique=True)
    email = db.Column(db.VARCHAR)
    password = db.Column(db.TEXT)
    card_num = db.Column(db.VARCHAR, unique=True)
    num_slots = db.Column(db.Integer)
    sub_date = db.Column(db.Date)

    def __init__(self, name, username, email, password, card_num, num_slots, sub_date):
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.card_num = card_num
        self.num_slots = num_slots
        self.sub_date = sub_date

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'email': self.email,
            'num_slots': self.num_slots,
            'sub_date': self.sub_date,
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


class UserSlots(db.Model):
    __tablename__ = 'user_slots'

    user_id = db.Column(db.Integer, primary_key=True)
    slot_num = db.Column(db.Integer, primary_key=True)
    tv_show_id = db.Column(db.Integer)

    def __init__(self, user_id, slot_num, tv_show_id):
        self.user_id = user_id
        self.slot_num = slot_num
        self.tv_show_id = tv_show_id


class DisplayUserSlots:
    def __init__(self, slots):
        self.slots = slots

    def serialize(self):
        return {
            'slots': [slot.serialize() for slot in self.slots]
        }


class Slot:
    def __init__(self, slot_num, tv_show_title, image_url):
        self.slot_num = slot_num
        self.tv_show_title = tv_show_title
        self.image_url = image_url

    def serialize(self):
        return {
            'slot_num': self.slot_num,
            'tv_show_title': self.tv_show_title,
            'image_url': self.image_url,
        }

