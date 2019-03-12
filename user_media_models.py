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
    date_added = db.Column(db.Date)
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


class UserRatedMovie:
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
