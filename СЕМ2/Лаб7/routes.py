from flask             import Blueprint, render_template, redirect, url_for
from config            import app, db
from flask_login       import LoginManager, login_user, logout_user, login_required, current_user
from models            import SignInForm, SignUpForm, Users
from werkzeug.security import generate_password_hash, check_password_hash
from config             import limiter

lab = Blueprint('lab', __name__, template_folder='templates')

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@lab.route('/lab/', methods=['GET'])
@login_required
def profile():
    return render_template('index.html', name=current_user.name)

@lab.route('/lab/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        name     = form.name.data
        email    = form.email.data
        password = form.password.data

        existing_user = Users.query.filter_by(email=email).first()

        if existing_user:
            message = 'Пользователь с указанным email уже существует'
            return render_template('login.html', form=form, message=message)
        else:
            new_user = Users(name=name, email=email, password = generate_password_hash(password))

            login_user(new_user)

            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('index'))
    else:
        message = 'Проверьте правильность введенных данных'

    return render_template('signup.html', form=form, message=message)


@lab.route('/lab/login', methods=['GET', 'POST'])
@limiter.limit('10/minute')
def login():
    form = SignInForm()

    if form.validate_on_submit():
        email    = form.email.data
        password = form.password.data

        user = Users.query.filter_by(email=email).first()

        if not user:
            message = 'Пользователь не найден'
            return render_template('login.html', form=form, message=message), 400

        if not check_password_hash(user.password, password):
            message = 'Неверный пароль'
            return render_template('login.html', form=form, message=message), 400

        login_user(user)
        return redirect(url_for('index')), 200
    else:
        print(form.errors)
        message = 'Проверьте правильность введенных данных'

    return render_template('login.html', form=form, message=message), 400


@lab.route('/lab/logout', methods=['GET'])
@login_required
def logout_get():
    logout_user()
    return redirect(url_for('login'))
