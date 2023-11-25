from flask_sqlalchemy import SQLAlchemy
from main import app

db = SQLAlchemy()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/SEM2LR5'
app.config['SQLAlchemy_TRACK_MODIFIVATTION'] = False

db.init_app(app)