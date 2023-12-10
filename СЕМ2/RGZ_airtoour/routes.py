from flask import Blueprint, render_template, redirect, url_for, request, get_flashed_messages
from flask_login       import LoginManager, login_user, current_user, login_required, logout_user
from config            import app, db
from models            import Users, OperationForm, Operation, SignInForm, OperationAdd
from datetime          import datetime, timedelta
from flask             import flash
from werkzeug.security import check_password_hash

operation = Blueprint('operation', __name__, template_folder='templates')

login_manager            = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(name):
    return Users.query.get(name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')

        user = Users.query.filter_by(name=name).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('operation.view_operation', lang='ru'))
        else:
            err_message = 'Такого пользователя не существует или введен неверный пароль!'
            return render_template('login.html', err_message=err_message)

    return render_template('login.html')


@app.route('/registration', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        is_user = Users.query.filter_by(email=email).first()

        if is_user:
            err_message = f'Пользователь с таким именем {name} уже существует!'
            return render_template('registration.html', err_message=err_message)
        else:
            try:
                new_user = Users(name=name, email=email)
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.commit()

                login_user(new_user)

                return redirect(url_for('operation.view_operation', lang='ru'))
            except Exception as e:
                db.session.rollback()
                err_message = 'Произошла какая-то ошибка!'
                app.logger.error(str(e))
                return render_template('registration.html', err_message=err_message)

    return render_template('registration.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    err_message = 'Вы вышли из аккаунта'
    return render_template('login.html', err_message=err_message)


@operation.route('/<lang>', methods=['GET', 'POST'])
@login_required
def view_operation(lang='ru'):
    form = OperationForm()

    if form.validate_on_submit():
        from_date = form.fromDate.data
        end_date = form.endDate.data
    else:
        end_date = datetime.utcnow()
        from_date = end_date - timedelta(days=30)

    operations = Operation.query.filter_by(user_id=current_user.id).filter(Operation.oper_date.between(from_date, end_date)).all()

    total_income  = sum(op.amount for op in operations if op.amount >= 0)
    total_expense = sum(op.amount for op in operations if op.amount < 0)

    return render_template(f'{lang}-operation.html', form=form, operations=operations, total_income=total_income, total_expense=total_expense)

@operation.route('/add', methods=['GET', 'POST'])
@login_required
def add_operation():
    form = OperationAdd()
    if form.validate_on_submit():
        oper_id   = form.id.data
        oper_type = form.oper_type.data
        amount    = form.amount.data
        date      = form.date.data
        user_id   = form.user_id.data

        if Operation.query.filter_by(id=oper_id).first():
            err_message = f'Операция с таким ID: {oper_id} уже существует!'
        else:
            try:
                operations = Operation(id=oper_id, oper_type=oper_type, amount=amount, date=date, user_id=user_id)
                db.session.add(operations)
                db.session.commit()
                err_message = f'Операция {oper_id} успешно добавлена!'
            except:
                db.session.rollback()
                err_message = 'Произошла ошибка во время добавления!'
    else:
        err_message = 'Неправильно введены данные, попробуйте снова.'

    return render_template('add_operation.html', form=form, err_message=err_message)