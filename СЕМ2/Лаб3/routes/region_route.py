from flask  import Blueprint, request, jsonify
from config import database
from models import Region, CarTaxParam, AreaTaxParam

region = Blueprint('regions', __name__)


@region.route("/v1/region/add", methods = ['POST'])
def add_region():
    try:
        region_code = request.json['region_code']
        region_name = request.json['region_name']
        region      = Region.query.filter(Region.id.equal(region_code)).all()

        if not region:
            region_code = Region(id = region_code)
            region_name = Region(name = region_name)
            database.session.add(region_name)
            database.session.add(region_code)
            database.session.commit()
            return jsonify({'message': f'Регион {region_name} успешно добавлен!'}), 200
        else:
            return jsonify({'error': f'Регион {region_name} уже существует!'}), 400
    except:
        return jsonify({'error': 'Произошла техническая ошибка во время добавления региона!'}), 400


@region.route("/v1/region/update", methods = ['POST'])
def update_region():
    try:
        region_code = request.json['region_code']
        region_name = request.json['region_name']
        region      = Region.query.filter(Region.id.equal(region_code)).all()
        if not region:
            return jsonify({'error': f'Регион {region_name} не существует!'}), 400
        else:
            Region.query.filter_by(id = region_code).update({'name': region_name})
            CarTaxParam.query.filter_by(city_id = region_code).update({'name': region_name})
            AreaTaxParam.query.filter_by(city_id = region_code).update({'name': region_name})
            database.session.commit()
            return jsonify({'message': f'Регион {region_name} успешно обновлён!'}), 200
    except:
        return jsonify({'error': 'Произошла техническая ошибка во время добавления региона!'}), 400


@region.route("/v1/region/delete", methods = ['POST'])
def delete_region():
    try:
        region_code = request.json['region_code']
        region = Region.query.filter(Region.id.equal(region_code)).all()
        if not region:
            return jsonify({'error': f'Регион {region_code} не существует!'}), 400
        else:
            Region.query.filter_by(id=region_code).delete()
            CarTaxParam.query.filter_by(city_id=region_code).delete()
            AreaTaxParam.query.filter_by(city_id=region_code).delete()
            database.session.commit()
            return jsonify({'message': f'Регион {region_code} успешно удалён!'}), 200
    except:
        return jsonify({'error': 'Произошла техническая ошибка во время добавления региона!'}), 400


@region.route("/v1/region/get", methods = ['GET'])
def get_region(id):
    try:
        region = list(map(lambda x: x.getData(), Region.query.filter_by(id = id).all()))
        return jsonify({'message': region}), 200
    except:
        return jsonify({'error': 'Произошла техническая ошибка!'}), 400


@region.route("/v1/region/get/all", methods = ['GET'])
def get_all_region():
    try:
        region = list(map(lambda x: x.getData(), Region.query.all()))
        return jsonify({'message': region}), 200
    except:
        return jsonify({'error': 'Произошла техническая ошибка!'}), 400