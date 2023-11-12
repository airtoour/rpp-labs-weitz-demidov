from flask import Blueprint, request, jsonify
from region_route import AreaTaxParam
from config import database

area_route = Blueprint('area_route', __name__)


@area_route.route("/v1/area/tax-param/add", methods = ['POST'])
def add_area():
    try:
        region_code = request.json['city_id']
        tax         = request.json['tax_rate']
        regions     = AreaTaxParam.query.filter(AreaTaxParam.city_id.equal(region_code)).all()

        if not regions:
            new_data = AreaTaxParam(region_code, tax)
            database.session.add(new_data)
            database.session.commit()
            return jsonify({'message': f'Местный налог по ID {region_code} успешно добавлен!'}), 200
        else:
            return jsonify({'error': f'Местный налог по ID {region_code} уже существует!'}), 400
    except:
        return jsonify({'error': 'Произошла техническая ошибка во время добавления региона!'}), 400


@area_route.route("/v1/area/tax-param/update", methods = ['POST'])
def update_area():
    try:
        region_code = request.json['city_id']
        tax         = request.json['tax_rate']
        region      = AreaTaxParam.query.filter(AreaTaxParam.city_id.equal(region_code)).all()
        if not region:
            return jsonify({'error': f'Регион {region_code} не существует!'}), 400
        else:
            AreaTaxParam.query.filter_by(city_id=region_code).update({'city_id': region_code, 'tax_rate': tax})
            database.session.commit()
            return jsonify({'message': f'Местный налог по ID {region_code} успешно обновлён!'}), 200
    except:
        return jsonify({'error': 'Произошла техническая ошибка во время добавления региона!'}), 400


@area_route.route("/v1/area/tax-param/delete", methods = ['POST'])
def delete_area():
    try:
        region_code = request.json['city_id']
        region      = AreaTaxParam.query.filter(AreaTaxParam.city_id.equal(region_code)).all()
        if not region:
            return jsonify({'error': f'Регион {region_code} не существует!'}), 400
        else:
            AreaTaxParam.query.filter_by(city_id=region_code).delete()
            database.session.commit()
            return jsonify({'message': f'Налог у региона {region_code} успешно удалён!'}), 200
    except:
        return jsonify({'error': 'Произошла техническая ошибка во время добавления региона!'}), 400


@area_route.route("/v1/area/tax-param/get", methods = ['GET'])
def get_area_tax(id):
    try:
        data = list(map(lambda x: x.getDataArea(), AreaTaxParam.query.filter_by(id = id).all()))
        return jsonify({'message': data}), 200
    except:
        return jsonify({'error': 'Произошла техническая ошибка!'}), 400


@area_route.route("/v1/area/tax-param/get", methods = ['GET'])
def get_area_tax_all():
    try:
        data = list(map(lambda x: x.getDataArea(), AreaTaxParam.query.all()))
        return jsonify({'message': data}), 200
    except:
        return jsonify({'error': 'Произошла техническая ошибка!'}), 400


@area_route.route("/v1/area/tax/calc", methods = ['GET'])
def area_tax_calc(id, cadastr):
    try:
        data = list(map(lambda x: x.getDataArea(), AreaTaxParam.query.filter_by(id=id).all()))
        rate = int(data[2]) * int(cadastr)
        return jsonify({'message': rate}), 200
    except:
        return jsonify({'error': 'Произошла техническая ошибка!'}), 400
