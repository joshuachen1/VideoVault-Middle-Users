import pymysql

from app import db


class dbCursor:
    def __init__(self, user):
        db_info = DB_Info.query.filter_by(user=user).first()
        dbHost = db_info.host
        dbUser = db_info.user
        dbPassword = db_info.password
        dbName = db_info.name
        charSet = 'utf8mb4'
        cusrorType = pymysql.cursors.DictCursor
        connectionObject = pymysql.connect(host=dbHost, user=dbUser, password=dbPassword, db=dbName, charset=charSet,
                                           cursorclass=cusrorType)


class DBInfo(db.Model):
    __tablename__ = 'db_info'
    
    host = db.Column(db.VARCHAR, primary_key=True)
    user = db.Column(db.VARCHAR)    
    password = db.Column(db.VARCHAR)    
    name = db.Column(db.VARCHAR)
    
    def __init__(self):
        pass
