from flask_wtf import FlaskForm
from flask_login import UserMixin
from wtforms import (IntegerField, FloatField, StringField, EmailField,
                     PasswordField, DateField, SubmitField, SelectField)
from wtforms.validators import DataRequired, InputRequired, Length, Email
from config import db

class Users(db.Model, UserMixin):
    id  = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    email = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        id = self.id
        name = self.name
        email = self.email
        password = self.password

        return f'Пользователь: {id}, {name}, {email}, {password}'

class RegistrationForm(FlaskForm):
    name = StringField('Имя пользователя: ', validators=[DataRequired()])
    password = PasswordField('Пароль: ', validators=[DataRequired(), Length(min=6, max=32)])
    email = EmailField('Электронная почта: ', validators=[DataRequired(), Email()])

class Login(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[InputRequired()])

class FindOperation(FlaskForm):
    from_date = DateField('Начало: ', validators=[DataRequired()])
    end_date = DateField('Конец: ', validators=[DataRequired()])
    submit = SubmitField('Найти')

class DbOperation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    operation_type = db.Column(db.String(12), nullable=False)
    operation_amount = db.Column(db.Float, nullable=False)
    operation_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class AddOperation(FlaskForm):
    id = IntegerField('Номер операции: ', validators=[DataRequired()])
    operation_type = SelectField('Тип операции: ', choices=[(1, "Доход"), (2, "Расход")], validators=[DataRequired()])
    operation_amount = FloatField('Сумма: ', validators=[DataRequired()])
    operation_date = DateField('Дата операции: ', validators=[DataRequired()])
    submit = SubmitField('Добавить операцию')

class DeleteOperation(FlaskForm):
    id = IntegerField('Номер операции: ')
    submit = SubmitField('Удалить операцию')