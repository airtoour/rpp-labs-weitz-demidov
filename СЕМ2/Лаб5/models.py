from flask_wtf          import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired
from config             import db



class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)


class RegionForm(FlaskForm):
    region_code = IntegerField('Код региона', validators=[DataRequired()])
    name = StringField('Название региона', validators=[DataRequired()])
    submit = SubmitField('Добавить')
    submit_update = SubmitField('Обновить')


class CarTaxParam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)
    from_hp_car = db.Column(db.Integer, nullable=False)
    to_hp_car = db.Column(db.Integer, nullable=False)
    from_production_year_car = db.Column(db.Integer, nullable=False)
    to_production_year_car = db.Column(db.Integer, nullable=False)
    rate = db.Column(db.Numeric, nullable=False)


class RegionFormDelete(FlaskForm):
    region_code = IntegerField('Код региона', validators=[DataRequired()])
    submit_delete = SubmitField('Удалить')


class TaxRouteForm(FlaskForm):
    code_rate = IntegerField('Код параметра', validators=[DataRequired()])
    year = IntegerField('Год выпуска автомобиля', validators=[DataRequired()])
    horsepower = IntegerField('Мощность автомобиля (л.с.)', validators=[DataRequired()])
    submit = SubmitField('Рассчитать налог')


class TaxParamForm(FlaskForm):
    code_rate = IntegerField('Код параметра', validators=[DataRequired()])
    region_code = IntegerField('Код региона', validators=[DataRequired()])
    from_hp_car = IntegerField('С какого количества лошадиных сил действует объект налогообложения',
                               validators=[DataRequired()])
    to_hp_car = IntegerField('До какого количества лошадиных сил действует объект налогообложения',
                             validators=[DataRequired()])
    from_production_year_car = IntegerField(
        'С какого года производства автомобиля действует объект налогообложения', validators=[DataRequired()])
    to_production_year_car = IntegerField('До какого года производства автомобиля действует объект налогообложения',
                                          validators=[DataRequired()])
    rate = FloatField('Налоговая ставка', validators=[DataRequired()])
    submit = SubmitField('Добавить')
    submit_update = SubmitField('Обновить')

class TaxParamForm_delete(FlaskForm):
    code_rate = IntegerField('Код параметра', validators=[DataRequired()])
    submit_delete = SubmitField('Удалить')