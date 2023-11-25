from flask  import Blueprint, request, render_template
from models import Region, RegionForm, CarTaxParam, RegionFormDelete, PlusMinusForm
from config import db

region = Blueprint('region', __name__, template_folder='templates')


@region.route('/list', methods=['GET'])
def region_list():
    form = RegionForm(request.form)
    regions = Region.query.all()
    return render_template('region-list.html', regions=regions, form=form)


@region.route('/add', methods=['GET', 'POST'])
def add_region():
    form = RegionForm(request.form)
    if form.validate_on_submit():
        region_code = form.region_code.data
        name = form.name.data

        if Region.query.filter_by(id=region_code).first():
            message = 'Регион с этим кодом уже существует'
        else:
            regions = Region(id=region_code, name=name)
            db.session.add(regions)
            db.session.commit()
            message = 'Регион успешно добавлен'
        return render_template('region-add.html', form=form, message=message)

    else:
        message = 'Проверьте правильность введенных данных'
    return render_template('region-add.html', form=form, message=message)


@region.route('/update', methods=['GET', 'POST'])
def update_region():
    form = RegionForm(request.form)
    if form.validate_on_submit():
        region_code = form.region_code.data
        name = form.name.data

        regions = Region.query.filter_by(id=region_code).first()
        if not regions:
            message = 'Региона с таким кодом не существует'
        else:
            regions.name = name
            db.session.commit()

            message = 'Регион успешно обновлен'
        return render_template('region-update.html', form=form, message=message)

    else:
        message = 'Проверьте правильность введенных данных'
    return render_template('region-update.html', form=form, message=message)


@region.route('/delete', methods=['GET', 'POST'])
def delete_region():
    form = RegionFormDelete(request.form)
    if form.validate_on_submit():
        region_code = form.region_code.data

        # Удаляем запись из таблицы tax_param
        tax_param = CarTaxParam.query.filter_by(city_id=region_code).first()
        if tax_param:
            db.session.delete(tax_param)
            db.session.commit()

        region = Region.query.filter_by(id=region_code).first()
        if not region:
            message = 'Региона с таким кодом не существует'
        else:
            db.session.delete(region)
            db.session.commit()
            message = 'Регион успешно удалён'
        return render_template('region-delete.html', form=form, message=message)

    else:
        message = 'Проверьте правильность введенных данных'
    return render_template('region-delete.html', form=form, message=message)


@region.route('/minus_plus_numbers', methods=['GET', 'POST'])
def plus_minus():
    form = PlusMinusForm(request.form)

    if form.validate_on_submit():
        number_one = form.number_one.data
        number_two = form.number_two.data
        operation  = form.operation.data

        if operation == '+':
            message = str(number_one + number_two)
        elif operation == '-':
            message = str(number_one - number_two)
        else:
            message = ''
    else:
        message = 'Проверьте правильность введенных данных'
        #message += f'\nErrors: {form.errors}'

    return render_template('plus-minus.html', form=form, message=message)