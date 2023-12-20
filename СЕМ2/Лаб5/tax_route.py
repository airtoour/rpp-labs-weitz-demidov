from flask import Blueprint, request, render_template
from models import TaxRouteForm, CarTaxParam, AddingNumsForm

tax = Blueprint('tax_route', __name__, template_folder='templates')


@tax.route('/', methods=['GET'])
def get_calculate_tax():
    form = TaxRouteForm(request.form)
    return render_template('index.html', form=form)


@tax.route('/calc', methods=['GET', 'POST'])
def calculate_tax():
    form = TaxRouteForm(request.form)
    if form.validate_on_submit():
        code_rate  = form.code_rate.data
        year       = form.year.data
        horsepower = form.horsepower.data

        tax_object = CarTaxParam.query.filter_by(id=code_rate). \
            filter(CarTaxParam.from_production_year_car <= year). \
            filter(CarTaxParam.to_production_year_car >= year). \
            filter(CarTaxParam.from_hp_car <= horsepower). \
            filter(CarTaxParam.to_hp_car >= horsepower).first()

        if not tax_object:
            message = 'Объект налогообложения по заданным параметрам не найден'
        else:
            tax_rate = tax_object.rate
            tax_calc = horsepower * tax_rate
            message = f'Налог на автомобиль с мощностью {horsepower} л.с. составит {tax_calc} руб.'
        return render_template('index.html', form=form, message=message)

    else:
        message = 'Проверьте правильность введенных данных'
    return render_template('index.html', form=form, message=message)

# Это эндпоинт для задания, а, то есть отдельный сайт
# Импорт необходимых модулей и классов.
# Ссылка будет такая: http://127.0.0.1:5000/tax/zadanie
@tax.route('/zadanie', methods=['GET', 'POST'])
def adding_numbs():
    # Создание экземпляра формы AddingNumsForm
    form = AddingNumsForm()

    # Проверка, была ли отправлена форма методом POST и прошла ли валидацию
    if form.validate_on_submit():
        # Если форма прошла валидацию, получаем данные из полей формы
        number_1 = form.number_1.data
        number_2 = form.number_2.data

        # Вычисление суммы введенных чисел
        result = number_1 + number_2

        # Формирование сообщения с результатом
        message = f'Результат: {result}'

        # Отображение шаблона 'zadanie.html' с формой и сообщением
        return render_template('zadanie.html', form=form, message=message)

    # Если форма не была отправлена или не прошла валидацию, отображаем шаблон 'zadanie.html' с формой
    return render_template('zadanie.html', form=form)
