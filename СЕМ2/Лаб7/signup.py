from flask import Blueprint, request, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from config import db

signup = Blueprint('signup', __name__)


@signup.route('/web/signup', methods=['GET'])
def signup_get():
    form = UserForm(request.form)
    return render_template('signup.html', form=form)

@signup.route('/v1/signup', methods=['POST'])
def signup_1():
    form = UserForm(request.form)
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        existing_user = Users.query.filter_by(email=email).first()
        if existing_user:
            message =  'Пользователь с указанным email уже существует'
            return render_template('signup.html', form=form, message=message)

        new_user = Users(name=name, email=email, password = generate_password_hash(password, method='pbkdf2:sha256'))
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login.login_get'))

    else:
        message = 'Проверьте правильность введенных данных'
    return render_template('signup.html', form=form, message=message)
