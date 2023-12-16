from flask_wtf import FlaskForm
from flask_login import UserMixin
from wtforms import EmailField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, Length, Email
from config import db

class Users(db.Model, UserMixin):
    id       = db.Column(db.Integer,     primary_key=True)
    email    = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), unique=True)
    name     = db.Column(db.String(255))

class SignInForm(FlaskForm):
    email = EmailField("Email: ", validators=[DataRequired()])
    password = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=6, max=32)])
    submit = SubmitField("Войти")


class SignUpForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired()])
    email = EmailField("Email: ", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=6, max=32)])
    submit = SubmitField("Зарегистрироваться")