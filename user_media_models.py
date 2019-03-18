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

    def __init__(self, title, year, service, tag, url, date_added, image_url):
        self.title = title
        self.year = year
        self.service = service
        self.tag = tag
        self.url = url
        self.date_added = date_added
        self.image_url = image_url

    def __repr__(self):
        return '<id {}>'.format(self.id)

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

    def __init__(self, title, year, num_seasons, num_episodes, service, tag, url, date_added, image_url):
        self.title = title
        self.year = year
        self.num_seasons = num_seasons
        self.num_episodes = num_episodes
        self.service = service
        self.tag = tag
        self.url = url
        self.date_added = date_added
        self.image_url = image_url

    def __repr__(self):
        return '<id {}>'.format(self.id)

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
        }


class UserRatedMedia:
    def __init__(self, title, rating):
        self.title = title
        self.rating = rating

    def __repr__(self):
        return '<title {} rating {}>'.format(self.title, self.rating)

    def serialize(self):
        return {
            'title': self.title,
            'rating': self.rating,
        }
