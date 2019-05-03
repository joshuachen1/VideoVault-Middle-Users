from app import db


# Models Regarding the movies Database
class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR)
    year = db.Column(db.VARCHAR)
    service = db.Column(db.VARCHAR)
    tag = db.Column(db.VARCHAR)
    url = db.Column(db.VARCHAR)
    date_added = db.Column(db.DATE)
    image_url = db.Column(db.VARCHAR)
    avg_rating = db.Column(db.REAL)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'year': self.year,
            'service': self.service,
            'tag': self.tag,
            'url': self.url,
            'date_added': self.date_added,
            'image_url': self.image_url,
            'avg_rating': self.avg_rating,
        }


class TVShows(db.Model):
    __tablename__ = 'tv_shows'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR)
    year = db.Column(db.VARCHAR)
    num_seasons = db.Column(db.INTEGER)
    num_episodes = db.Column(db.INTEGER)
    service = db.Column(db.VARCHAR)
    tag = db.Column(db.VARCHAR)
    url = db.Column(db.VARCHAR)
    date_added = db.Column(db.DATE)
    image_url = db.Column(db.VARCHAR)
    avg_rating = db.Column(db.REAL)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'year': self.year,
            'num_seasons': self.num_seasons,
            'num_episodes': self.num_episodes,
            'service': self.service,
            'tag': self.tag,
            'url': self.url,
            'date_added': self.date_added,
            'image_url': self.image_url,
            'avg_rating': self.avg_rating,
        }


class MovieComment(db.Model):
    __tablename__ = 'movie_comments'

    movie_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    comment = db.Column(db.VARCHAR)
    date_of_comment = db.Column(db.DateTime, primary_key=True)

    def __init__(self, movie_id, user_id, comment, date_of_comment):
        self.movie_id = movie_id
        self.user_id = user_id
        self.comment = comment
        self.date_of_comment = date_of_comment


class TVShowComment(db.Model):
    __tablename__ = 'tv_show_comments'

    tv_show_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    comment = db.Column(db.VARCHAR)
    date_of_comment = db.Column(db.DateTime, primary_key=True)

    def __init__(self, tv_show_id, user_id, comment, date_of_comment):
        self.tv_show_id = tv_show_id
        self.user_id = user_id
        self.comment = comment
        self.date_of_comment = date_of_comment


class Comment:
    def __init__(self, user_id, username, comment, date_of_comment):
        self.user_id = user_id
        self.username = username
        self.comment = comment
        self.date_of_comment = date_of_comment

    def serialize(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'comment': self.comment,
            'date_of_comment': self.date_of_comment,
        }
