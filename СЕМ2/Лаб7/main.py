# #from config import app
# from routes import lab
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
# from flask_login import LoginManager
# from models import Users
#
#
# app = Flask(__name__)
# db = SQLAlchemy()
#
# app.register_blueprint(lab, url_prefix='/lab')
#
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/SEM2LR6'
# app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
# app.config['WTF_CSRF_ENABLED'] = False
# app.secret_key = 'airtooooour'
#
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'
#
# @login_manager.user_loader
# def load_user(user_id):
#     return Users.query.get(int(user_id))
#
#
# db.init_app(app)
#
# limiter = Limiter(get_remote_address,
#                   app            = app,
#                   default_limits = ["10 per minute"],
#                   storage_uri    = "memory://")
#
# if __name__ == '__main__':
#     app.run(debug=True)
