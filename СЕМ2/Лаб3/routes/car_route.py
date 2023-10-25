from flask import Blueprint, request
from routes.region_route import Region, CarTaxParam
from Config import db

cars = Blueprint('cars',__name__)

@cars.route("/v1/car/tax-param/add", methods = ['POST'])
def AddCar():
    try:
        car_id = request.json['id']
        city_id = request.json['city_id']
        from_hp_car = request.json['from_hp_car']
        to_hp_car = request.json['to_hp_car']
        from_production_year_car = request.json['from_production_year_car']
        to_production_year_car = request.json['to_production_year_car']
        rate = request.json['rate']

        regions = Region.query.filter(Region.id.equal(city_id)).all()
        car_id = CarTaxParam.query.filter(CarTaxParam.car_id.equal(car_id)).all()
        region_in_car_table = CarTaxParam.query.filter(CarTaxParam.city_id.equal(city_id)).all()
        from_hp_car_in_table = CarTaxParam.query.filter(CarTaxParam.from_hp_car.equal(from_hp_car)).all()
        to_hp_car_in_table = CarTaxParam.query.filter(CarTaxParam.to_hp_car.equal(to_hp_car)).all()
        from_production_year_car_in_table = CarTaxParam.query.filter(CarTaxParam.from_production_year_car.equal(from_production_year_car)).all()
        to_production_year_car_in_table = CarTaxParam.query.filter(CarTaxParam.to_production_year_car.equal(to_production_year_car)).all()

        if regions is None:
            return {'data is not exist'}, 400
        elif regions and car_id and region_in_car_table and from_hp_car_in_table and to_hp_car_in_table and from_production_year_car_in_table and to_production_year_car_in_table:
            return {'data exist'}, 200
        else:
            new_data = CarTaxParam(car_id, city_id, from_hp_car, to_hp_car, from_production_year_car,
                                   to_production_year_car, rate)
            db.session.add(new_data)
            db.session.commit()
            return {'done'}, 200
    except:
        {'error'}, 400



@cars.route("/v1/car/tax-param/update", methods = ['POST'])
def UpdateCar():
    try:
        car_id = request.json['id']
        city_id = request.json['city_id']
        from_hp_car = request.json['from_hp_car']
        to_hp_car = request.json['to_hp_car']
        from_production_year_car = request.json['from_production_year_car']
        to_production_year_car = request.json['to_production_year_car']
        rate = request.json['rate']

        regions = Region.query.filter(Region.id.equal(city_id)).all()
        car_id = CarTaxParam.query.filter(CarTaxParam.car_id.equal(car_id)).all()
        region_in_car_table = CarTaxParam.query.filter(CarTaxParam.city_id.equal(city_id)).all()
        from_hp_car_in_table = CarTaxParam.query.filter(CarTaxParam.from_hp_car.equal(from_hp_car)).all()
        to_hp_car_in_table = CarTaxParam.query.filter(CarTaxParam.to_hp_car.equal(to_hp_car)).all()
        from_production_year_car_in_table = CarTaxParam.query.filter(CarTaxParam.from_production_year_car.equal(from_production_year_car)).all()
        to_production_year_car_in_table = CarTaxParam.query.filter(CarTaxParam.to_production_year_car.equal(to_production_year_car)).all()

        if regions is None:
            return {'data is not exist'}, 400
        elif regions and car_id and region_in_car_table and from_hp_car_in_table and to_hp_car_in_table \
                and from_production_year_car_in_table and to_production_year_car_in_table:
            return {'data exist'}, 200
        else:
            CarTaxParam.query.filter_by(id=car_id).update({'city_id': city_id, 'from_hp_car': from_hp_car,
                'to_hp_car': to_hp_car, 'from_production_year_car': from_production_year_car, 'to_production_year_car': to_production_year_car, 'rate': rate})
            db.session.commit()
            return {'done'}, 200
    except:
        {'error'}, 400



@cars.route("/v1/car/tax-param/delete", methods = ['POST'])
def DeleteCar():
    try:
        city_id = request.json['city_id']
        regions = Region.query.filter(Region.id.equal(city_id)).all()
        car = CarTaxParam.query.filter(CarTaxParam.city_id.equal(city_id)).all()
        if regions and car:
            CarTaxParam.query.filter_by(city_id=city_id).delete()
            db.session.commit()
            return {'done'}, 200
        else:
            return {'data is not exist'}, 400
    except:
        {'error'}, 400



@cars.route("/v1/car/tax-param/get", methods = ['GET'])
def GetDataCar(id):
    try:
        car_data = list(map(lambda x: x.getDataCar(), Region.query.filter_by(car_id=id).all()))
        return car_data, 200
    except:
        {'error'}, 400



@cars.route("/v1/car/tax-param/get/all", methods = ['GET'])
def GetDataCar(all):
    try:
        car_data = list(map(lambda x: x.getDataCar(), CarTaxParam.query.all()))
        return car_data, 200
    except:
        {'error'}, 400



@cars.route("/v1/car/tax/calc", methods = ['GET'])
def GetDataCar(id, year, hp):
    try:
        car_data = list(map(lambda x: x.getDataCar(), CarTaxParam.query.all()))
        if int(car_data[2]) < int(hp) <= int(car_data[3]) and int(car_data[4]) < int(year) <= int(car_data[5]):
            calc = int(car_data[6]) * int(hp)
            return calc, 200
    except:
        {'error'}, 400