from app import db


class Key(db.Model):
    __tablename__ = 'security'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.TEXT)

    def __init__(self):
        pass
