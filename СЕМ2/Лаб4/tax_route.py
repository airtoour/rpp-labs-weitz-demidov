from flask import Blueprint, render_template, request
from models import CarTaxParam, AreaTaxParam

tax = Blueprint("tax", __name__, template_folder='templates')

@tax.route('/')
def index():
    return render_template("index.html")

@tax.route('/calc', methods=['GET', 'POST'])
def tax_calc():
    city_id = request.form.get('city_id')
    horse_power = request.form.get('to_hp_car')
    tax_rate = request.form.get('tax_rate')

    if city_id:
        if horse_power and tax_rate:
            hp_model = CarTaxParam(city_id=city_id, to_hp_car=horse_power)
            tax_model = AreaTaxParam(city_id=city_id, tax_rate=tax_rate)
            result = hp_model * tax_model

            message = f'Новая ставка равна {result}'

            return render_template('index.html', hp_model=hp_model, tax_model=tax_model, message=message)
    else:
        message = ''
        return render_template('index.html', message=message)