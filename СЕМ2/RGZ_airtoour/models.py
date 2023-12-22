from flask_wtf          import FlaskForm
from flask_login        import UserMixin
from werkzeug.security  import generate_password_hash, check_password_hash
from wtforms            import (IntegerField, FloatField, StringField, EmailField,
                                PasswordField, DateField, SubmitField, SelectField, validators)
from wtforms.validators import DataRequired, InputRequired, Length
from config             import db
from flask_babel        import _

class Users(db.Model, UserMixin):
    id       = db.Column(db.Integer,     primary_key=True)
    name     = db.Column(db.String(60),  nullable=False, unique=True)
    email    = db.Column(db.String(60),  nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class SignUpForm(FlaskForm):
    name     = StringField('Логин: ',  validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6, max=32)])
    email    = EmailField('Эл. почта', validators=[DataRequired(), validators.Email()])
    submit   = SubmitField('Регистрация')

class SignInForm(FlaskForm):
    name     = StringField('Логин: ',    validators=[DataRequired()])
    password = PasswordField('Пароль: ', validators=[InputRequired()])
    submit   = SubmitField('Войти')


class OperationAddDb(db.Model):
    id        = db.Column(db.Integer,                            primary_key=True)
    oper_type = db.Column(db.String(12),                         nullable=False)
    amount    = db.Column(db.Float,                              nullable=False)
    oper_date = db.Column(db.DateTime,                           nullable=False)
    user_id   = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class OperationAdd(FlaskForm):
    id        = IntegerField('Номер операции:',                                     validators=[DataRequired()])
    oper_type = SelectField('Тип операции:', choices=[(1, "Доход"), (2, "Расход")], validators=[DataRequired()])
    amount    = FloatField('Сумма:',                                                validators=[DataRequired()])
    oper_date = DateField('Дата операции:',                                         validators=[DataRequired()])
    user_id   = IntegerField('Номер пользователя:',                                 validators=[DataRequired()])
    submit    = SubmitField('Добавить операцию')


class OperationFormRu(FlaskForm):
    fromDate = DateField(_('Начало: '), validators=[DataRequired()])
    endDate  = DateField(_('Конец: '),  validators=[DataRequired()])
    submit   = SubmitField(_('Найти'))

class OperationFormEn(FlaskForm):
    fromDate = DateField(_('Start Date: '), validators=[DataRequired()])
    endDate  = DateField(_('End Date: '),   validators=[DataRequired()])
    submit   = SubmitField(_('Find'))