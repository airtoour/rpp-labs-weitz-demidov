from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Region(db.Model):
    id   = db.Column(db.Integer,    primary_key = True)
    name = db.Column(db.String(64), nullable    = False)

    def get_region(self):
        try:
            return jsonify({'message': f"<ID региона: {self.id}; Имя региона: {self.name}>"}), 200
        except Exception:
            return jsonify({'error': f"Региона с таким ID: {self.id} и именем: {self.name} не существует!"}), 400

class CarTaxParam(db.Model):
    id                       = db.Column(db.Integer,                             primary_key = True)
    city_id                  = db.Column(db.Integer, db.ForeignKey('region.id'), nullable    = False)
    from_hp_car              = db.Column(db.Integer,                             nullable    = False)
    to_hp_car                = db.Column(db.Integer,                             nullable    = False)
    from_production_year_car = db.Column(db.Integer,                             nullable    = False)
    to_production_year_car   = db.Column(db.Integer,                             nullable    = False)
    tax_rate                 = db.Column(db.Numeric,                             nullable    = False)

    def get_car_tax_params(self):
        try:
            return jsonify({'message': f'< Tax ID:                 {self.id};'
                                       f'City ID:                  {self.city_id};'
                                       f'From HP car:              {self.from_hp_car};'
                                       f'To HP car:                {self.to_hp_car};'
                                       f'From production year car: {self.from_production_year_car};'
                                       f'To production year car:   {self.to_production_year_car};'
                                       f'Tax Rate:                 {self.tax_rate}>'}), 200
        except Exception:
            return jsonify({'error': f"Данных с регионом {self.city_id} не существует в таблице car_tax_param!"})


class AreaTaxParam(db.Model):
    id       = db.Column(db.Integer,                             primary_key = True)
    city_id  = db.Column(db.Integer, db.ForeignKey('Region.id'), nullable    = False)
    tax_rate = db.Column(db.Numeric,                             nullable    = False)

    def get_area_tax_params(self):
        try:
            return jsonify({'message': f'<Tax ID:   {self.id}; '
                                       f'Region ID: {self.city_id}; '
                                       f'Tax Rate:  {self.tax_rate}>'}), 200
        except Exception:
            return jsonify({'error': f"Данных с регионом {self.city_id} не существует в таблице area_tax_param!"}), 400