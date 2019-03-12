from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pymysql
import os

# Setup App
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])  # Should change based on is in Development or Production
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS
CORS(app)

# Start Database
db = SQLAlchemy(app)

# Enable Variable Port for Heroku
port = int(os.environ.get('PORT', 33507))

# Import Models

# Force pymysql to be used as replacement for MySQLdb
pymysql.install_as_MySQLdb()


# [url]/
@app.route('/')
def hello_world():
    return 'Home Page'


if __name__ == '__main__':
    app.run(port=port)
