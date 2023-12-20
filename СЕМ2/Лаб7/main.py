###########################################
# Перед запуском просто в pgAdmin создайте базу, назовите ее SEM2LR7 и создайте таблицу, которая в файле table



from flask import render_template, redirect, url_for, Flask, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.fields.simple import EmailField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, Length, Email

# Для задания понадобится библиотека datetime
from datetime import datetime

app = Flask(__name__)
db = SQLAlchemy()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/SEM2LR7'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.secret_key = 'gleb'

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


# Задаем лимитер для эндпоинтов
limiter = Limiter(get_remote_address,
                  app=app,
                  # default_limits по умолчанию выставляем 5 в час, если не указано в эндпоинте @limiter.limit, значит будет это значение
                  default_limits=["5 per hour"],
                  storage_uri="memory://")

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
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


@app.route('/login', methods=['GET', 'POST'])
@limiter.limit('10/day')
def login():
    form = SignInForm()

    if request.method == 'POST':
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


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# ЗАДАНИЕ
@app.route('/zadaniye', methods=['GET', 'POST'])
@login_required
@limiter.limit("5/hour")
def zadaniye():
    # ЗАПИСЫВАЕМ В curr_date ТЕКУЩУЮ ДАТУ С ПОМОЩЬЮ datetime.utcnow()
    curr_date = datetime.utcnow()
    # ФАЙЛ ЗАДАНИЕ НАХОДИТСЯ В ПАПКЕ TEMPLATES
    return render_template('zadaniye.html', curr_date=curr_date)


db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
