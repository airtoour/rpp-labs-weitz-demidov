from flask             import render_template, redirect, url_for, request
from flask_login       import LoginManager, login_user, current_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from config            import app, db
from models            import SignUp, SignIn

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(name):
    return SignIn.query.get(name)

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

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        pass_hash = generate_password_hash(password)
        checked_pass = check_password_hash(pass_hash, password)

        is_user = Users.query.filter_by(email=email).first()
        if is_user:
            err_message = f'Пользователь с таким именем {name} уже существует!'
            return render_template('signup.html', err_message=err_message)

        if checked_pass:
            new_user = Users(name=name, email=email, password=pass_hash)
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)

            return redirect(url_for('index'))

    return render_template('signup.html')