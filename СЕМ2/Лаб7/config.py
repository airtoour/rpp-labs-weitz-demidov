from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# app = Flask(__name__)
# db = SQLAlchemy()
#
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/SEM2LR6'
# app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
# app.config['WTF_CSRF_ENABLED'] = False
# app.secret_key = 'airtooooour'
#
# db.init_app(app)
#
# limiter = Limiter(get_remote_address,
#                   app            = app,
#                   default_limits = ["10 per minute"],
#                   storage_uri    = "memory://")