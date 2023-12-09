from flask_wtf          import FlaskForm
from wtforms            import StringField, IntegerField, EmailField, PasswordField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, Email
from config             import db

class SignUp(db.Model):
    name = db.Column(db.String(60), nullable=False)
    password = db.Column(db.Stirng(255), )

class SignUpForm(FlaskForm):
    name     = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль',         validators=[DataRequired(), Length(min=6, max=32)])
    email    = EmailField('Электронная почта', validators=[DataRequired(), Email()])

class SignIn(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль',     validators=[DataRequired()])

    def __repr__(self):
        name = self.name
        password = self.password

        return f'{name}, {password}'