from flask import Blueprint, render_template, request
from models import database, Region

region = Blueprint('region', __name__)

@region.route('/web/region', methods = ['GET'])
def show_regions():
    regions = Region.query.all()  # Получаем все регионы из базы данных
    return render_template('region-list.html', regions = regions)


@region.route('/web/region/add', methods = ['GET'])
def show_add_region():
    return render_template('region-add.html')

@region.route('/web/region/add', methods = ['POST'])
def add_region():
    # Логика добавления региона в базу данных
    region_code = request.form.get('id')
    region_name = request.form.get('name')

    if region_code and region_name:
        new_region_code = Region(id = region_code)
        new_region_name = Region(name = region_name)
        database.session.add(new_region_code)
        database.session.add(new_region_name)
        database.session.commit()
        message = f'Регион {region_code}, {region_name} успешно добавлен!'
    else:
        message = 'Произошла какая-то ошибка!'

    return render_template('region-add.html', message = message)


@region.route('/web/region/update', methods=['GET'])
def show_update_region():
    return render_template('region-update.html')

@region.route('/web/region/update', methods=['POST'])
def update_region():
    # Логика обновления региона в базе данных
    region_code = request.form.get('id')
    get_region = Region.query.get(region_code)

    if get_region:
        # Обновление данных региона
        get_region.name = request.form.get('name')
        database.session.commit()
        message = f'Регион {region_code} успешно обновлен!'
    else:
        message = f'Регион с ID {region_code} не найден в базе данных!'

    return render_template('region-update.html', message = message)


@region.route('/web/region/delete', methods=['GET'])
def show_delete_region():
    return render_template('region-delete.html')

@region.route('/web/region/delete', methods=['POST'])
def delete_region():
    # Логика удаления региона из базы данных
    region_code = request.form.get('id')
    get_region = Region.query.get(region_code)

    if get_region:
        # Удаление региона
        database.session.delete(get_region)
        database.session.commit()
        message = f'Регион {region_code} успешно удален!'
    else:
        message = f'Регион с ID {region_code} не найден в базе данных!'

    return render_template('region-delete.html', message = message)