# Configuration and initialization

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), 'app.db')
URI = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = URI
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)

from app import api
