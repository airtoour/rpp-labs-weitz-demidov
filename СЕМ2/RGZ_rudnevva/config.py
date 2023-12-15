from models import db
from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/Rudneva'
app.config['SQLAlchemy_TRACK_MODIFIVATTION'] = False
app.config['SECRET_KEY'] = 'rudneva_polina'

db.init_app()