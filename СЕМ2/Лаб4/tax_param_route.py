from flask import Blueprint, render_template, request
from models import database, Region, CarTaxParam

tax_param = Blueprint('tax_param', __name__)


@tax_param.route('/web/tax-param', methods=['GET'])
def show_tax_params():
    tax_params = CarTaxParam.query.all()  # Получаем все объекты налогообложения из базы данных
    return render_template('tax-param-list.html', tax_params=tax_params)


@tax_param.route('/web/tax-param/add', methods=['GET'])
def show_add_tax_param_form():
    return render_template('tax-param-add.html')

@tax_param.route('/web/tax-param/add', methods=['POST'])
def add_tax_param():
    # Получаем данные из формы
    city_id                  = request.form.get('city_id')
    from_hp_car              = request.form.get('from_hp_car')
    to_hp_car                = request.form.get('to_hp_car')
    from_production_year_car = request.form.get('from_production_year_car')
    to_production_year_car   = request.form.get('to_production_year_car')
    tax_rate                 = request.form.get('tax_rate')

    region = Region.query.filter(Region.id.equal(city_id)).all()

    if region:
        message = f'Регион {city_id} уже существует!'
    else:
        # Проверяем, что все поля заполнены
        if city_id and from_hp_car and to_hp_car and from_production_year_car and to_production_year_car and tax_rate:
            # Создаем новый объект налогообложения и добавляем его в базу данных
            new_tax_param = CarTaxParam(city_id                  = city_id,
                                        from_hp_car              = from_hp_car,
                                        to_hp_car                = to_hp_car,
                                        from_production_year_car = from_production_year_car,
                                        to_production_year_car   = to_production_year_car,
                                        tax_rate                 = tax_rate)
            database.session.add(new_tax_param)
            database.session.commit()
            message = 'Объект налогообложения успешно добавлен!'
        else:
            message = 'Пожалуйста, заполните все поля формы.'

    return render_template('tax-param-add.html', message=message)

@tax_param.route('/web/tax-param/update', methods=['GET'])
def show_update_tax_param_form():
    return render_template('tax-param-update.html')

@tax_param.route('/web/tax-param/update', methods=['POST'])
def show_update_tax_param():
    # Получаем данные из формы, что обновить
    city_id                  = request.form.get('city_id')
    from_hp_car              = request.form.get('from_hp_car')
    to_hp_car                = request.form.get('to_hp_car')
    from_production_year_car = request.form.get('from_production_year_car')
    to_production_year_car   = request.form.get('to_production_year_car')
    tax_rate                 = request.form.get('tax_rate')

    region = Region.query.filter(Region.id.equal(city_id)).all()

    if region:
        if from_hp_car or to_hp_car or from_production_year_car or to_production_year_car or tax_rate:
            # Логика обновления таблицы car_tax_param
            CarTaxParam.query.filter_by(city_id = city_id).update({'city_id':                  city_id,
                                                                   'from_hp_car':              from_hp_car,
                                                                   'to_hp_car':                to_hp_car,
                                                                   'from_production_year_car': from_production_year_car,
                                                                   'to_production_year_car':   to_production_year_car,
                                                                   'tax_rate':                 tax_rate})
            database.session.commit()
            message = 'Запись успешно обновлена!'
        else:
            message = f'Региона {city_id} не существует!'
    else:
        message = 'Произошла какая-то ошибка во время обновления таблицы!'

    return render_template('tax-param-add.html', message = message)


# Аналогично обработка роутов для удаления объектов налогообложения!!!!!!!!!!!!!!!!!!!!!
# Должна быть реализована логика для обновления и удаления объектов налогообложения в базе данных
# Возвращение сообщений об успешности или неудаче операций также аналогично описанному в предыдущем примере