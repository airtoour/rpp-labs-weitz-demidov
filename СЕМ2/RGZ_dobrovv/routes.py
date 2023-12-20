from flask import Blueprint, render_template, redirect, url_for, request
from flask_login       import LoginManager, login_user, current_user, login_required, logout_user
from config            import app, db
from models            import Users, OperationForm, OperationAdd, Operation, SignInForm, SignUpForm
from datetime          import datetime, timedelta

operation = Blueprint('operation', __name__, template_folder='templates')

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(name):
    return Users.query.get(name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = SignInForm()

    if form.validate_on_submit():
        name     = form.name.data
        password = form.password.data

        user = Users.query.filter_by(name=name).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('operation.view_operation'))
        else:
            err_message = 'Такого пользователя не существует или введен неверный пароль!'
            return render_template('login.html', form=form, err_message=err_message)

    return render_template('login.html', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = SignUpForm()

    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        email = form.email.data

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

                return render_template('registration.html', form=form, err_message=err_message)

    return render_template('registration.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    form = SignInForm()

    logout_user()
    err_message = 'Вы вышли из аккаунта'
    return render_template('login.html', form=form, err_message=err_message)


@operation.route('/', methods=['GET', 'POST'])
@login_required
def view_operation():
    form = OperationForm()
    message = None

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


    today = datetime.utcnow().date()
    today_operation = Operation.query.filter_by(operation_date=today).first()

    if not today_operation:
        message = 'У Вас нет расходов за сегодня. Пожалуйста, добавьте операции расходов через кнопку ниже!'

    return render_template('operation.html', form=form, operations=operations,
                           total_income=total_income, total_expense=total_expense,
                           message=message)

@operation.route('/add', methods=['GET', 'POST'])
@login_required
def add_operation():
    form = OperationAdd()

    if request.method == 'POST':
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
