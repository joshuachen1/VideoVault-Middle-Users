from app import db


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
    profile_pic = db.Column(db.VARCHAR)
    slots_to_delete = db.Column(db.Integer)

    def __init__(self, name, username, email, password, card_num, num_slots, sub_date, profile_pic):
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.card_num = card_num
        self.num_slots = num_slots
        self.sub_date = sub_date
        self.profile_pic = profile_pic
        self.slots_to_delete = 0

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'email': self.email,
            'num_slots': self.num_slots,
            'sub_date': self.sub_date,
            'profile_pic': self.profile_pic,
            'slots_to_delete': self.slots_to_delete
        }


class Friends(db.Model):
    __tablename__ = 'user_friend_list'

    user_id = db.Column(db.Integer, primary_key=True)
    friend_id = db.Column(db.Integer, primary_key=True)

    def __init__(self, user_id, friend_id):
        self.user_id = user_id
        self.friend_id = friend_id


class PendingFriends(db.Model):
    __tablename__ = 'pending_friends'

    user_id = db.Column(db.Integer, primary_key=True)
    pending_from_id = db.Column(db.Integer, primary_key=True)

    def __init__(self, user_id, pending_from_id):
        self.user_id = user_id
        self.pending_from_id = pending_from_id


class TimeLine(db.Model):
    __tablename__ = 'user_timeline'

    post_id = db.Column(db.Integer, primary_key=True)
    wall_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    post = db.Column(db.VARCHAR)
    date_of_post = db.Column(db.DateTime)

    def __init__(self, wall_id, user_id, post, date_of_post):
        self.wall_id = wall_id
        self.user_id = user_id
        self.post = post
        self.date_of_post = date_of_post


class Post:
    def __init__(self, post_id, user_id, username, post_user_id, post_username, post, date_of_post, comments):
        self.post_id = post_id
        self.user_id = user_id
        self.username = username
        self.post_user_id = post_user_id
        self.post_username = post_username
        self.post = post
        self.date_of_post = date_of_post
        self.comments = comments

    def serialize(self):
        return {
            'post_id': self.post_id,
            'user_id': self.user_id,
            'username': self.username,
            'post_user_id': self.post_user_id,
            'post_username': self.post_username,
            'post': self.post,
            'date_of_post': self.date_of_post,
            'comments': [comment.serialize() for comment in self.comments],
        }


class PostComments(db.Model):
    __tablename__ = 'post_comments'

    comment_id = db.Column(db.Integer, primary_key=True)
    wall_id = db.Column(db.Integer)
    post_user_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    comment = db.Column(db.VARCHAR)
    date_of_comment = db.Column(db.DateTime)
    post_id = db.Column(db.Integer)

    def __init__(self, wall_id, post_user_id, user_id, comment, date_of_comment, post_id):
        self.wall_id = wall_id
        self.post_user_id = post_user_id
        self.user_id = user_id
        self.comment = comment
        self.date_of_comment = date_of_comment
        self.post_id = post_id


class PostComment:
    def __init__(self, user_id, username, post_user_id, post_username, comment_user_id, comment_username, comment,
                 date_of_comment):
        self.user_id = user_id
        self.username = username
        self.post_user_id = post_user_id
        self.post_username = post_username
        self.comment_user_id = comment_user_id
        self.comment_username = comment_username
        self.comment = comment
        self.date_of_comment = date_of_comment

    def serialize(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'post_user_id': self.post_user_id,
            'post_username': self.post_username,
            'comment_user_id': self.comment_user_id,
            'comment_username': self.comment_username,
            'comment': self.comment,
            'date_of_comment': self.date_of_comment,
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


class DisplayRatedMovie:
    def __init__(self, user_id, rated_movies):
        self.user_id = user_id
        self.rated_movies = rated_movies

    def serialize(self):
        return {
            'user_id': self.user_id,
            'rated_movies': [rm.serialize() for rm in self.rated_movies]
        }


class RatedMovie:
    def __init__(self, movie_id, movie_title, image_url, user_rating):
        self.movie_id = movie_id
        self.movie_title = movie_title
        self.image_url = image_url
        self.user_rating = user_rating

    def serialize(self):
        return {
            'movie_id': self.movie_id,
            'movie_title': self.movie_title,
            'image_url': self.image_url,
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


class DisplayRatedTVShow:
    def __init__(self, user_id, rated_tv_shows):
        self.user_id = user_id
        self.rated_tv_shows = rated_tv_shows

    def serialize(self):
        return {
            'user_id': self.user_id,
            'rated_tv_shows': [rts.serialize() for rts in self.rated_tv_shows]
        }


class RatedTVShow:
    def __init__(self, tv_show_id, tv_show_title, image_url, user_rating):
        self.tv_show_id = tv_show_id
        self.tv_show_title = tv_show_title
        self.image_url = image_url
        self.user_rating = user_rating

    def serialize(self):
        return {
            'tv_show_id': self.tv_show_id,
            'tv_show_title': self.tv_show_title,
            'image_url': self.image_url,
            'rating': self.user_rating,
        }


class UserSlots(db.Model):
    __tablename__ = 'user_slots'

    user_id = db.Column(db.Integer, primary_key=True)
    slot_num = db.Column(db.Integer, primary_key=True)
    tv_show_id = db.Column(db.Integer)
    unsubscribe = db.Column(db.BOOLEAN)
    delete_slot = db.Column(db.BOOLEAN)

    def __init__(self, user_id, slot_num, tv_show_id):
        self.user_id = user_id
        self.slot_num = slot_num
        self.tv_show_id = tv_show_id
        self.unsubscribe = False
        self.delete_slot = False


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


class UserRentedMovies(db.Model):
    __tablename__ = 'user_rented_movies'

    user_id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, primary_key=True)
    rent_datetime = db.Column(db.DATETIME)

    def __init__(self, user_id, movie_id, rent_datetime):
        self.user_id = user_id
        self.movie_id = movie_id
        self.rent_datetime = rent_datetime
