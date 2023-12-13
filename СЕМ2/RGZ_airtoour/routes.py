from flask import Blueprint, render_template, redirect, url_for
from flask_login       import LoginManager, login_user, current_user, login_required, logout_user
from config            import app, db
from models            import (Users, OperationFormRu, OperationFormEn, OperationAddDb, OperationAdd,
                               SignInForm, SignUpForm)
from datetime          import datetime, timedelta
from flask_babel       import Babel, _

babel = Babel(app)
babel.init_app(app, default_locale='ru')

operation = Blueprint('operation', __name__, template_folder='templates')

login_manager            = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(name):
    return Users.query.get(name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = SignInForm()
    err_message = None

    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data

        user = Users.query.filter_by(name=name).first()

        if user.check_password(password):
            login_user(user)
            return redirect(url_for('operation.view_operation', lang='ru'))
        else:
            err_message = 'Неправильно введен пароль или логин, попробуйте ещё раз.'

    return render_template('login.html', form=form, err_message=err_message)


@app.route('/registration', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        name     = form.name.data
        email    = form.email.data
        password = form.password.data

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

    return render_template('registration.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@operation.route('/<lang>', methods=['GET', 'POST'])
@login_required
def view_operation(lang='ru'):
    if lang == 'en':
        form = OperationFormEn()
        form.fromDate.label.text = _('Start Date')
        form.endDate.label.text = _('End Date')
        form.submit.label.text = _('Find')
    else:
        form = OperationFormRu()

    if form.validate_on_submit():
        from_date = form.fromDate.data
        end_date = form.endDate.data
    else:
        end_date = datetime.utcnow()
        from_date = end_date - timedelta(days=30)

    operations = OperationAddDb.query.filter_by(
        user_id=current_user.id).filter(OperationAddDb.oper_date.between(from_date, end_date)).all()

    total_income  = sum(op.amount for op in operations if op.amount >= 0)
    total_expense = sum(op.amount for op in operations if op.amount < 0)

    return render_template(f'{lang}-operation.html', form=form, operations=operations,
                           total_income=total_income, total_expense=total_expense)

@operation.route('/add', methods=['GET', 'POST'])
@login_required
def add_operation():
    form = OperationAdd()

    if form.validate_on_submit():
        oper_id   = form.id.data
        oper_type = form.oper_type.data
        amount    = form.amount.data
        date      = form.oper_date.data
        user_id   = form.user_id.data

        if OperationAddDb.query.filter_by(id=oper_id).first():
            message = f'Операция с таким ID: {oper_id} уже существует!'
        else:
            try:
                operations = OperationAddDb(id=oper_id, oper_type=oper_type, amount=amount, oper_date=date, user_id=user_id)
                db.session.add(operations)
                db.session.commit()
                message = f'Операция {oper_id} успешно добавлена!'
            except Exception as e:
                db.session.rollback()
                app.logger.error(f'Error during operation addition: {str(e)}')
                message = 'Произошла ошибка во время добавления!'

        return render_template('add_operation.html', form=form, message=message)

    return render_template('add_operation.html', form=form)