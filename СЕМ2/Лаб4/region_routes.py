from flask import Blueprint, render_template, request
from models import database, Region  # Предполагается, что у вас есть модель Region в файле models.py

region = Blueprint('region', __name__)

@region.route('/web/region', methods = ['GET'])
def show_regions():
    regions = Region.query.all()  # Получаем все регионы из базы данных
    return render_template('region-list.html', regions = regions)


@region.route('/web/region/add', methods = ['GET'])
def show_add_region_form():
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
        message = 'Регион успешно добавлен!'
    else:
        message = 'Произошла какая-то ошибка!'
    return render_template('region-add.html', message = message)


@region.route('/web/region/update', methods=['GET'])
def show_update_region_form():
    return render_template('region-update.html')

@region.route('/web/region/update', methods=['POST'])
def update_region():
    # Логика обновления региона в базе данных
    # Аналогично добавлению, но с использованием Region.query.get(id) для получения объекта из базы данных
    region_code = Region.query.get(id)

    if region_code:
        Region.query.filter_by(id=region_code).update({'id': region_code})
    return render_template('region-update.html', message = message)

@region.route('/web/region/delete', methods=['GET'])
def show_delete_region_form():
    return render_template('region-delete.html')

@region.route('/web/region/delete', methods=['POST'])
def delete_region():
    # Логика удаления региона из базы данных
    # Аналогично добавлению, но с использованием Region.query.get(id) для получения объекта из базы данных
    # Подробности реализации зависят от вашей логики удаления
    return render_template('region-delete.html', message=message)