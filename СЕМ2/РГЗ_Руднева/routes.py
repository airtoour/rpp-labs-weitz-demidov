from flask import render_template, redirect, url_for
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from config import app, db
from models import Users, Login, Registration, FindOperation, Operation, AddOperation, DeleteOperation
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(name):
    return Users.query.get(name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()

    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data

        user = Users.query.filter_by(name=name).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('find_operation'))
        else:
            error_message = 'Такого пользователя не существует или введен неверный пароль!'
            return render_template('login.html', form=form, error_message=error_message)

    return render_template('login.html', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = Registration()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        hashed_password = generate_password_hash(password)

        user = Users.query.filter_by(email=email).first()

        if user:
            error_message = 'Пользователь уже существует!'
            return render_template('registration.html', form=form, error_message=error_message)
        else:
            new_user = Users(name=name, email=email, password=hashed_password)

            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)

            return redirect(url_for('find_operation'))

    return render_template('registration.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    form = Login()
    err_message = 'Вы вышли из аккаунта'
    return render_template('login.html', form=form, err_message=err_message)


@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('find_operation'))
    else:
        return redirect(url_for('login'))


@app.route('/operation', methods=['GET', 'POST'])
@login_required
def find_operation():
    form = FindOperation()

    if form.validate_on_submit():
        from_date = form.from_date.data
        end_date = form.end_date.data
    else:
        end_date = datetime.utcnow()
        from_date = end_date - timedelta(days=30)

    operations = Operation.query.filter_by(
        user_id=current_user.id).filter(Operation.operation_date.between(from_date, end_date)).all()

    total_income  = sum(op.operation_amount for op in operations if op.operation_amount >= 0)
    total_expense = sum(op.operation_amount for op in operations if op.operation_amount < 0)

    return render_template('operation.html', form=form, operations=operations, from_date=from_date, end_date=end_date,
                           total_income=total_income, total_expense=total_expense)


@app.route('/add-operation', methods=['GET', 'POST'])
@login_required
def add_operation():
    form = AddOperation()

    if form.validate_on_submit():
        oper_id = form.id.data
        oper_type = form.operation_type.data
        amount = form.operation_amount.data
        date = form.operation_date.data
        user_id = current_user.id

        oper = Operation.query.filter_by(id=oper_id).first()

        if oper:
            message = 'Такая операция уже существует!'
        else:
            try:
                operations = Operation(id=oper_id, operation_type=oper_type, operation_amount=amount,
                                       operation_date=date, user_id=user_id)
                db.session.add(operations)
                db.session.commit()

                message = f'Операция на сумму {amount} успешно добавлена!'
            except:
                db.session.rollback()
                message = 'Ошибка во время добавления операции!'

        return render_template('add-operation.html', form=form, message=message)

    return render_template('add-operation.html', form=form)


@app.route('/delete-operation', methods=['GET', 'POST'])
@login_required
def delete_operation():
    form = DeleteOperation()

    if form.validate_on_submit():
        oper_id = form.id.data

        operations = Operation.query.filter_by(id=oper_id).first()

        if operations:
            db.session.delete(operations)
            db.session.commit()

            return redirect(url_for('find_operation'))
        else:
            message = f'Операции {oper_id} не существует.'
            render_template('delete-operation.html', form=form, message=message)

    return render_template('delete-operation.html', form=form)
