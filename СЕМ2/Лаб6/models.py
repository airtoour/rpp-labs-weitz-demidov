from flask_login import UserMixin
from config import db

class Users(db.Model, UserMixin):
    id       = db.Column(db.Integer,     primary_key=True)
    email    = db.Column(db.String(60),  nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    name     = db.Column(db.String(255), nullable=False, unique=True)

    def __repr__(self):
        id = self.id
        email = self.email
        password = self.password
        name = self.name

        return f'{id}, {name}, {email}, {password}'