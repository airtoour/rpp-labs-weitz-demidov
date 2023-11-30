from flask             import render_template, redirect, url_for, request
from flask_login       import LoginManager, login_user, current_user, login_required
from werkzeug.security import check_password_hash
from models            import Users
from config            import app
import time

login_manager = LoginManager(app)
login_manager.login_view = 'login'

max_requests      = 10
current_requests  = 0
last_request_time = time.time()


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route('/index', methods = ['GET', 'POST'])
@login_required
def index():
    if current_user.is_authenticated:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Users.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            err_message = 'Такого пользователя не существует!'
            return render_template('signup.html', err_message=err_message)

    return render_template('login.html')