from flask import Blueprint, render_template, request
from models import db, Region

region = Blueprint('region', __name__, template_folder='templates')

@region.route('/list', methods=['GET', 'POST'])
def show_regions():
    regions = Region.query.all()
    return render_template('region-list.html', regions=regions)


@region.route('/add', methods=['GET', 'POST'])
def add_region():
    # Логика добавления региона в базу данных
    region_code = request.form.get('id')
    region_name = request.form.get('name')

    if region_code:
        if region_code and region_name:
            new_region = Region(id=region_code, name=region_name)
            db.session.add(new_region)
            db.session.commit()
            message = f'Регион {region_code}, {region_name} успешно добавлен!'
        else:
            db.session.rollback()
            message = 'Произошла ошибка во время добавление региона!'
    else:
        message = ''

    return render_template('region-add.html', message=message)


@region.route('/update', methods=['GET', 'POST'])
def update_region():
    # Логика обновления региона в базе данных
    region_code = request.form.get('id')
    get_region = Region.query.get(region_code)

    if get_region:
        if get_region:
            # Обновление данных региона
            get_region.name = request.form.get('name')
            db.session.commit()

            message = f'Регион {region_code} успешно обновлен!'
        elif not get_region:
            db.session.rollback()
            message = f'Регион с ID {region_code} не найден в базе данных!'
        else:
            db.session.rollback()
            message = 'Произошла ошибка во время добавления региона!'
    else:
        message = ''

    return render_template('region-update.html', message=message)


@region.route('/delete', methods=['GET', 'POST'])
def delete_region():
    # Логика удаления региона из базы данных
    region_code = request.form.get('id')
    get_region = Region.query.get(region_code)

    if get_region:
        if get_region:
            # Удаление региона
            db.session.delete(get_region)
            db.session.commit()
            message = f'Регион {region_code} успешно удален!'
        elif not get_region:
            db.session.rollback()
            message = f'Регион с ID {region_code} не найден в базе данных!'
        else:
            db.session.rollback()
            message = 'Произошла ошибка во время добавление региона!'
    else:
        message = ''

    return render_template('region-delete.html', message = message)


@region.route('/numbers/a=<int:a>&b=<int:b>', methods=['GET', 'POST'])
def show_numbers(a, b):
    show_a = a
    show_b = b

    return render_template('numbers.html', a=show_a, b=show_b)