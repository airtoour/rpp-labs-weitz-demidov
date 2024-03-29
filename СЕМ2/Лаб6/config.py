from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)

db = SQLAlchemy()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/SEM2LR6'
app.config['SQLAlchemy_TRACK_MODIFIVATTION'] = False
app.config['SECRET_KEY'] = 'airtoour_shiva'

db.init_app(app)