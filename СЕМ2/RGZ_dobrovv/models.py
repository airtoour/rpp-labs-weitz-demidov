from flask_wtf import FlaskForm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import (IntegerField, FloatField, StringField, EmailField,
                     PasswordField, DateField, SubmitField, SelectField)
from wtforms.validators import DataRequired, InputRequired, Length, Email
from config import db

class Users(db.Model, UserMixin):
    id  = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    email = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class SignUpForm(FlaskForm):
    name     = StringField('Имя пользователя: ', validators=[DataRequired()])
    password = PasswordField('Пароль: ', validators=[DataRequired(), Length(min=6, max=32)])
    email    = EmailField('Электронная почта: ', validators=[DataRequired(), Email()])

class SignInForm(FlaskForm):
    name     = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[InputRequired()])

class OperationDb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    operation_type = db.Column(db.String(12), nullable=False)
    operation_amount = db.Column(db.Float, nullable=False)
    operation_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Operation(FlaskForm):
    id = IntegerField('Номер операции: ', validators=[DataRequired()])
    operation_type = SelectField('Тип операции: ', choices=[(1, "Доход"), (2, "Расход")], validators=[DataRequired()])
    operation_amount = FloatField('Сумма: ', validators=[DataRequired()])
    operation_date = DateField('Дата операции: ', validators=[DataRequired()])
    user_id = IntegerField('Номер пользователя: ', validators=[DataRequired()])
    submit = SubmitField('Добавить операцию')

class OperationForm(FlaskForm):
    from_date = DateField('Начало: ', validators=[DataRequired()])
    end_date = DateField('Конец: ', validators=[DataRequired()])
    submit = SubmitField('Найти')