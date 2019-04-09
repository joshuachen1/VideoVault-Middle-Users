from app import db


class DBInfo(db.Model):
    __tablename__ = 'db_info'

    host = db.Column(db.VARCHAR, primary_key=True)
    user = db.Column(db.VARCHAR)
    password = db.Column(db.VARCHAR)
    name = db.Column(db.VARCHAR)

    def __init__(self):
        pass
