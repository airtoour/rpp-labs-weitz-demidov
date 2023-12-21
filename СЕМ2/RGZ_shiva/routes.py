from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from config import app, db
from models import Users, OperationForm, Operation, OperationAdd, OperationUpdate, Signin, Signup
from datetime import datetime, timedelta

operation = Blueprint('operation', __name__, template_folder='templates')

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(name):
    return Users.query.get(name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Signin()

    if request.method == 'POST':
        name = form.name.data
        password = form.password.data

        user = Users.query.filter_by(name=name).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('operation.find_operation'))
        else:
            err_message = 'Такого пользователя не существует или введен неверный пароль!'
            return render_template('login.html', err_message=err_message)

    return render_template('login.html', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = Signup()

    if request.method == 'POST':
        name = form.name.data
        email = form.email.data
        password = form.password.data

        available_user = Users.query.filter_by(email=email).first()

        if available_user:
            err_message = f'Пользователь с таким именем {name} уже существует!'
            return render_template('registration.html', err_message=err_message)
        else:
            try:
                new_user = Users(name=name, email=email)
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.commit()

                login_user(new_user)

                return redirect(url_for('operation.find_operation'))
            except:
                db.session.rollback()
                err_message = 'Произошла какая-то ошибка!'

                return render_template('registration.html', form=form, err_message=err_message)

    return render_template('registration.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    form = Signin()
    logout_user()
    err_message = 'Вы вышли из аккаунта'
    return render_template('login.html', form=form, err_message=err_message)


@operation.route('/', methods=['GET', 'POST'])
@login_required
def find_operation():
    form = OperationForm()

    if form.validate_on_submit():
        from_date = form.from_date.data
        end_date = form.end_date.data
    else:
        end_date = datetime.utcnow()
        from_date = end_date - timedelta(days=30)

    operations = Operation.query.filter_by(
        user_id=current_user.id).filter(Operation.oper_date.between(from_date, end_date)).all()

    total_income  = sum(op.amount for op in operations if op.amount >= 0)
    total_expense = sum(op.amount for op in operations if op.amount < 0)

    return render_template('operation.html', form=form, operations=operations,
                           total_income=total_income, total_expense=total_expense)

@operation.route('/add-oper', methods=['GET', 'POST'])
@login_required
def add_operation():
    form = OperationAdd()

    if request.method == 'POST':
        oper_id = form.id.data
        oper_type = form.oper_type.data
        amount = form.amount.data
        date = form.oper_date.data
        user_id = current_user.id

        oper = Operation.query.filter_by(id=oper_id).first()

        if oper:
            message = 'Такая операция уже существует!'
        else:
            try:
                operations = Operation(id=oper_id, oper_type=oper_type, amount=amount,
                                       oper_date=date, user_id=user_id)
                db.session.add(operations)
                db.session.commit()

                message = f'Операция на сумму {amount} успешно добавлена!'
            except Exception as e:
                db.session.rollback()
                app.logger.error(f"Ошибка во время добавления операции: {e}")
                message = 'Ошибка во время добавления операции!'

        return render_template('add-operation.html', form=form, message=message)

    return render_template('add-operation.html', form=form)


@operation.route('/change-operation', methods=['GET', 'POST'])
@login_required
def change_operation():
    form = OperationUpdate()
    message = None

    if request.method == 'POST':
        oper_id = form.id.data
        oper_type = form.oper_type.data
        amount = form.amount.data
        date = form.oper_date.data
        user_id = current_user.id

        operations = Operation.query.filter_by(id=oper_id).first()

        if not operations:
            message = 'Такой операции не существует :('
        else:
            if operations.oper_type or operations.amount or operations.date or operations.user_id:
                operations.oper_type = oper_type
                operations.amount = amount
                operations.date = date
                operations.user_id = user_id

                db.session.commit()

                message = 'Операция успешно обновлена!'
            else:
                message = 'Вы не выбрали ни одного поля для заполнения.'

    return render_template('change-operation.html', form=form, message=message)
