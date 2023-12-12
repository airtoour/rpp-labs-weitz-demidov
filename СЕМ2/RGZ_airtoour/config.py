from flask            import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/SEM2RGR'
app.config['SQLAlchemy_TRACK_MODIFIVATTION'] = False
app.config['SECRET_KEY'] = 'airtoour'

db.init_app(app)