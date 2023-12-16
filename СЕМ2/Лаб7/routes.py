from flask import Blueprint, request, render_template, redirect, url_for
from config import app, db
from flask_login import login_user, login_required
from models import SignInForm, SignUpForm, Users


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        name     = form.name.data
        email    = form.email.data
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

@app.route('/web/login', methods=['GET'])
def login_get():
    form = UserForm(request.form)
    return render_template('login.html', form=form)


@app.route('/v1/login', methods=['POST'])
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


@app.route('/web/logout', methods=['GET'])
@login_required
def logout_get():
    logout_user()
    return redirect(url_for('login.login_get'))


@app.route('/', methods=['GET'])
@login_required
def profile():
    return render_template('index.html', name=current_user.name)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))