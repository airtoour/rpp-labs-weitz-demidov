from flask import Blueprint, render_template, request
from models import db, Region, CarTaxParam

tax_param = Blueprint('tax_param', __name__)


@tax_param.route('/list', methods=['GET', 'POST'])
def show_tax_params():
    # Получаем все объекты налогообложения из базы данных
    tax_params = CarTaxParam.query.all()
    return render_template('tax-param-list.html', tax_params=tax_params)


@tax_param.route('/add', methods=['GET', 'POST'])
def add_tax_param():
    # Получаем данные из формы
    city_id                  = request.form.get('city_id')
    from_hp_car              = request.form.get('from_hp_car')
    to_hp_car                = request.form.get('to_hp_car')
    from_production_year_car = request.form.get('from_production_year_car')
    to_production_year_car   = request.form.get('to_production_year_car')
    tax_rate                 = request.form.get('tax_rate')

    if city_id:
        # Проверяем, что все поля заполнены
        if city_id and from_hp_car and to_hp_car and from_production_year_car and to_production_year_car and tax_rate:
            # Создаем новый объект налогообложения и добавляем его в базу данных
            new_tax_param = CarTaxParam(city_id                  = city_id,
                                        from_hp_car              = from_hp_car,
                                        to_hp_car                = to_hp_car,
                                        from_production_year_car = from_production_year_car,
                                        to_production_year_car   = to_production_year_car,
                                        tax_rate                 = tax_rate)
            db.session.add(new_tax_param)
            db.session.commit()
            message = 'Объект налогообложения успешно добавлен!'
        else:
            db.session.rollback()
            message = 'Произошла ошибка во время добавления региона!'
    else:
        message = ''

    return render_template('tax-param-add.html', message=message)


@tax_param.route('/update', methods=['GET', 'POST'])
def update_tax_param():
    # Получаем данные из формы, для обновления
    city_id                  = request.form.get('city_id')
    from_hp_car              = request.form.get('from_hp_car')
    to_hp_car                = request.form.get('to_hp_car')
    from_production_year_car = request.form.get('from_production_year_car')
    to_production_year_car   = request.form.get('to_production_year_car')
    tax_rate                 = request.form.get('tax_rate')

    region = Region.query.filter_by(id=city_id).all()

    if region:
        if city_id or from_hp_car or to_hp_car or from_production_year_car or to_production_year_car or tax_rate:
            # Логика обновления таблицы car_tax_param
            CarTaxParam.query.filter_by(city_id=city_id).update({'city_id':                  city_id,
                                                                 'from_hp_car':              from_hp_car,
                                                                 'to_hp_car':                to_hp_car,
                                                                 'from_production_year_car': from_production_year_car,
                                                                 'to_production_year_car':   to_production_year_car,
                                                                 'tax_rate':                 tax_rate})
            db.session.commit()
            message = 'Запись успешно обновлена!'
        else:
            db.session.rollback()
            message = 'Произошла ошибка во время обновления региона!'
    else:
        message = f'Региона {city_id} не существует!'

    return render_template('tax-param-add.html', message=message)


@tax_param.route('/delete', methods=['GET', 'POST'])
def delete_tax_param():
    city_id = request.form.get('city_id')

    region = Region.query.filter_by(id=city_id).all()

    if region:
        if region:
            db.session.delete(city_id)
            db.session.commit()
            message = f'Объект налогообложения успешно удалён!'
        else:
            message = 'Такого региона не существует!'
    else:
        message = ''

    return render_template('tax-param-delete.html', message=message)