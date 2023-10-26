from flask import Blueprint, request, jsonify
from routes.region_route import Region, CarTaxParam
from config import database

cars = Blueprint('cars', __name__)

@cars.route("/v1/car/tax-param/add", methods = ['POST'])
def add_car():
    try:
        car_id                            = request.json['id']
        city_id                           = request.json['city_id']
        from_hp_car                       = request.json['from_hp_car']
        to_hp_car                         = request.json['to_hp_car']
        from_production_year_car          = request.json['from_production_year_car']
        to_production_year_car            = request.json['to_production_year_car']
        rate                              = request.json['tax_rate']

        region                            = Region.query.filter(Region.id.equal(city_id)).all()
        car_id                            = CarTaxParam.query.filter(CarTaxParam.car_id.equal(car_id)).all()
        region_in_car_table               = CarTaxParam.query.filter(CarTaxParam.city_id.equal(city_id)).all()
        from_hp_car_in_table              = CarTaxParam.query.filter(CarTaxParam.from_hp_car.equal(from_hp_car)).all()
        to_hp_car_in_table                = CarTaxParam.query.filter(CarTaxParam.to_hp_car.equal(to_hp_car)).all()
        from_production_year_car_in_table = CarTaxParam.query.filter(CarTaxParam.from_production_year_car.equal(from_production_year_car)).all()
        to_production_year_car_in_table   = CarTaxParam.query.filter(CarTaxParam.to_production_year_car.equal(to_production_year_car)).all()

        if region is None:
            return jsonify({'error': f'Регион {region} не существует!'}), 400
        elif region and car_id and region_in_car_table and from_hp_car_in_table and to_hp_car_in_table \
                and from_production_year_car_in_table and to_production_year_car_in_table:
            return jsonify({'message': f'Регион {region} уже существует!'}), 200
        else:
            new_data = CarTaxParam(car_id, city_id, from_hp_car, to_hp_car, from_production_year_car, to_production_year_car, rate)
            database.session.add(new_data)
            database.session.commit()
            return jsonify({'message': f'Машина {car_id} успешно добавлен!'}), 200
    except:
        return jsonify({'error': 'Произошла техническая ошибка во время добавления машины!'}), 400


@cars.route("/v1/car/tax-param/update", methods = ['POST'])
def update_car():
    try:
        car_id                            = request.json['id']
        city_id                           = request.json['city_id']
        from_hp_car                       = request.json['from_hp_car']
        to_hp_car                         = request.json['to_hp_car']
        from_production_year_car          = request.json['from_production_year_car']
        to_production_year_car            = request.json['to_production_year_car']
        rate                              = request.json['tax_rate']

        region                            = Region.query.filter(Region.id.equal(city_id)).all()
        car_id                            = CarTaxParam.query.filter(CarTaxParam.car_id.equal(car_id)).all()
        region_in_car_table               = CarTaxParam.query.filter(CarTaxParam.city_id.equal(city_id)).all()
        from_hp_car_in_table              = CarTaxParam.query.filter(CarTaxParam.from_hp_car.equal(from_hp_car)).all()
        to_hp_car_in_table                = CarTaxParam.query.filter(CarTaxParam.to_hp_car.equal(to_hp_car)).all()
        from_production_year_car_in_table = CarTaxParam.query.filter(CarTaxParam.from_production_year_car.equal(from_production_year_car)).all()
        to_production_year_car_in_table   = CarTaxParam.query.filter(CarTaxParam.to_production_year_car.equal(to_production_year_car)).all()

        if region is None:
            return jsonify({'error': f'Регион {region} не существует!'}), 400
        elif region and car_id and region_in_car_table and from_hp_car_in_table and to_hp_car_in_table \
                and from_production_year_car_in_table and to_production_year_car_in_table:
            return jsonify({'message': f'Регион {region} уже существует!'}), 200
        else:
            CarTaxParam.query.filter_by(id = car_id).update({'city_id':                  city_id,
                                                             'from_hp_car':              from_hp_car,
                                                             'to_hp_car':                to_hp_car,
                                                             'from_production_year_car': from_production_year_car,
                                                             'to_production_year_car':   to_production_year_car,
                                                             'tax_rate':                 rate})
            database.session.commit()
            return jsonify({'message': f'Машина {car_id} успешно обновлён!'}), 200
    except:
        return jsonify({'error': 'Произошла техническая ошибка во время обновления машины!'}), 400


@cars.route("/v1/car/tax-param/delete", methods = ['POST'])
def delete_car():
    try:
        city_id = request.json['city_id']
        region  = Region.query.filter(Region.id.equal(city_id)).all()
        car     = CarTaxParam.query.filter(CarTaxParam.city_id.equal(city_id)).all()
        if region and car:
            CarTaxParam.query.filter_by(city_id=city_id).delete()
            database.session.commit()
            return jsonify({'message': f'Машина {car} успешно удалён!'}), 200
        else:
            return jsonify({'error': f'Регион {region} не существует!'}), 400
    except:
        return jsonify({'error': 'Произошла техническая ошибка во время обновления машины!'}), 400


@cars.route("/v1/car/tax-param/get", methods = ['GET'])
def get_car_data(id):
    try:
        car_data = list(map(lambda x: x.getDataCar(), Region.query.filter_by(car_id=id).all()))
        return jsonify({'message': car_data}), 200
    except:
        return jsonify({'error': 'Произошла техническая ошибка!'}), 400


@cars.route("/v1/car/tax-param/get/all", methods = ['GET'])
def get_car_data_all():
    try:
        car_data = list(map(lambda x: x.getDataCar(), CarTaxParam.query.all()))
        return jsonify({'message': car_data}), 200
    except:
        return jsonify({'error': 'Произошла техническая ошибка!'}), 400


@cars.route("/v1/car/tax/calc", methods = ['GET'])
def get_calc_car_data(id, year, hp):
    try:
        car_data = list(map(lambda x: x.getDataCar(), CarTaxParam.query.all()))
        if int(car_data[2]) < int(hp) <= int(car_data[3]) and int(car_data[4]) < int(year) <= int(car_data[5]):
            calc = int(car_data[6]) * int(hp)
            return jsonify({'message': calc}), 200
    except:
        return jsonify({'error': 'Произошла техническая ошибка!'}), 400