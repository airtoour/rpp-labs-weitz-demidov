from flask_wtf import FlaskForm
from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from wtforms import StringField, SubmitField, BooleanField, PasswordField, EmailField
from wtforms.validators import DataRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_required, login_user, current_user, logout_user
from signup import Users
from config import db, login_manager
from limit import limiter

login = Blueprint('login', __name__)


class UserForm(FlaskForm):
    email = EmailField("Email: ", validators=[DataRequired()])
    password = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=6, max=32)])
    submit = SubmitField("Войти")



@login.route('/v1/login', methods=['POST'])
@limiter.limit('10/minute')
def login_1():
    form = UserForm(request.form)
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        remember = True if request.form.get('remember') else False
        user = Users.query.filter_by(email=email).first()

        if not user:
            message = 'Пользователь не найден'
            return render_template('login.html', form=form, message=message), 400

        if not check_password_hash(user.password, password):
            message = 'Неверный пароль'
            return render_template('login.html', form=form, message=message), 400

        login_user(user, remember=remember)
        return redirect(url_for('login.profile')), 200

    else:
        print(form.errors)
        message = 'Проверьте правильность введенных данных'
    return render_template('login.html', form=form, message=message), 400


@login.route('/web/logout', methods=['GET'])
@login_required
def logout_get():
    logout_user()
    return redirect(url_for('login.login_get'))


@login.route('/', methods=['GET'])
@login_required
def profile():
    return render_template('index.html', name=current_user.name)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
