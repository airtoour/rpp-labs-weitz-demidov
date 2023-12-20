from flask import render_template, redirect, url_for, Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.fields.simple import EmailField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, Length, Email

app = Flask(__name__)
db = SQLAlchemy()

limiter = Limiter(get_remote_address,
                  app=app,
                  default_limits=["10 per day"],
                  storage_uri="memory://")

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route('/lab/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', name=current_user.name)


@app.route('/lab/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        existing_user = Users.query.filter_by(email=email).first()

        if existing_user:
            message = 'Пользователь с указанным email уже существует'
            return render_template('login.html', form=form, message=message)
        else:
            new_user = Users(name=name, email=email, password=generate_password_hash(password))

            login_user(new_user)

            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('index'))
    else:
        message = 'Проверьте правильность введенных данных'

    return render_template('signup.html', form=form, message=message)


@app.route('/lab/login', methods=['GET', 'POST'])
@limiter.limit('10/day')
def login():
    form = SignInForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = Users.query.filter_by(email=email).first()

        if not user:
            message = 'Пользователь не найден'
            return render_template('login.html', form=form, message=message), 400

        if not check_password_hash(user.password, password):
            message = 'Неверный пароль'
            return render_template('login.html', form=form, message=message), 400

        login_user(user)
        return redirect(url_for('zadaniye')), 200
    else:
        print(form.errors)
        message = 'Проверьте правильность введенных данных'

    return render_template('login.html', form=form, message=message), 400


@app.route('/lab/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('lab.login'))


class UserForm(FlaskForm):
    email = EmailField("Email: ", validators=[DataRequired()])
    password = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=6, max=32)])
    submit = SubmitField("Войти")


@app.route('/lab/zadaniye', methods=['GET', 'POST'])
@login_required
@limiter.limit("10/day")
def zadaniye():
    return render_template('zadaniye.html', username=current_user.name)


@app.route('/', methods=['GET'])
@login_required
def profile():
    return render_template('index.html', name=current_user.name)


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255))


class SignInForm(FlaskForm):
    email = EmailField("Email: ", validators=[DataRequired()])
    password = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=6, max=32)])
    submit = SubmitField("Войти")


class SignUpForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired()])
    email = EmailField("Email: ", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=6, max=32)])
    submit = SubmitField("Зарегистрироваться")


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/SEM2LR6'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['WTF_CSRF_ENABLED'] = False
app.secret_key = 'airtooooour'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
