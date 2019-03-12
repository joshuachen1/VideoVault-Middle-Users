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
    __tablename__ = 'user_friends'

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
