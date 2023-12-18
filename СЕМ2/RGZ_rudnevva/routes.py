from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from config import app, db
from models import Users, OperationFindForm, OperationDb, Operation, OperationDelete
from datetime import datetime, timedelta

operation = Blueprint('operation', __name__, template_folder='templates')

login_manager = LoginManager(app)
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

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('operation.view_operation'))
        else:
            err_message = 'Такого пользователя не существует или введен неверный пароль!'
            return render_template('login.html', err_message=err_message)

    return render_template('login.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
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

                return redirect(url_for('operation.view_operation'))
            except Exception as e:
                db.session.rollback()
                app.logger.error(f"Произошла ошибка: {e}")
                err_message = 'Произошла какая-то ошибка!'

                return render_template('registration.html', err_message=err_message)

    return render_template('registration.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    err_message = 'Вы вышли из аккаунта'
    return render_template('login.html', err_message=err_message)


@operation.route('/', methods=['GET', 'POST'])
@login_required
def view_operation():
    form = OperationFindForm()

    if form.validate_on_submit():
        from_date = form.from_date.data
        end_date = form.end_date.data
    else:
        end_date = datetime.utcnow()
        from_date = end_date - timedelta(days=30)

    operations = OperationDb.query.filter_by(
        user_id=current_user.id).filter(OperationDb.operation_date.between(from_date, end_date)).all()

    total_income  = sum(op.operation_amount for op in operations if op.operation_amount >= 0)
    total_expense = sum(op.operation_amount for op in operations if op.operation_amount < 0)

    return render_template('operation.html', form=form, operations=operations,
                           total_income=total_income, total_expense=total_expense)

@operation.route('/add', methods=['GET', 'POST'])
@login_required
def add_operation():
    form = Operation()

    if form.validate_on_submit():
        oper_id = form.id.data
        oper_type = form.operation_type.data
        amount = form.operation_amount.data
        date = form.operation_date.data
        user_id = form.user_id.data

        if OperationDb.query.filter_by(id=oper_id).first():
            message = f'ID: {oper_id}. Такая операция уже существует!'
        else:
            try:
                operations = OperationDb(id=oper_id, operation_type=oper_type, operation_amount=amount,
                                         operation_date=date, user_id=user_id)
                db.session.add(operations)
                db.session.commit()
                message = f'Операция на сумму {amount} успешно добавлена!'
            except Exception as e:
                db.session.rollback()
                app.logger.error(f"Произошла ошибка: {e}")
                message = 'Произошла ошибка во время добавления!'

        return render_template('add-operation.html', form=form, message=message)

    return render_template('add-operation.html', form=form)

@operation.route('/delete-operation', methods=['GET', 'POST'])
@login_required
def delete_operation():
    form = OperationDelete()
    message = None

    if form.validate_on_submit():
        oper_id = form.id.data

        operations = OperationDb.query.filter_by(id=oper_id).first()
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