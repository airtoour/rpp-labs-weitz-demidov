from flask import Blueprint, request
from routes.region_route import Region, AreaTaxParam
from Config import db

area_route = Blueprint('area_route',__name__)


@area_route.route("/v1/area/tax-param/add", methods = ['POST'])
def AddArea():
    try:
        region_code = request.json['regione_code']
        tax = request.json['tax']
        regions = AreaTaxParam.query.filter(AreaTaxParam.city_id.equal(region_code)).all()
        if regions is None:
            new_data = AreaTaxParam(region_code, tax)
            db.session.add(new_data)
            db.session.commit()
            return {'done'}, 200
        else:
            return {'data exist'}, 400
    except:
        {'error'}, 400



@area_route.route("/v1/area/tax-param/update", methods = ['POST'])
def UpdateArea():
    try:
        region_code = request.json['regione_code']
        tax = request.json['tax']
        regions = AreaTaxParam.query.filter(AreaTaxParam.city_id.equal(region_code)).all()
        if regions is None:
            return {'data is not exist'}, 400
        else:
            AreaTaxParam.query.filter_by(city_id=region_code).update({'city_id': region_code, 'rate': tax})
            db.session.commit()
            return {'done'}, 200
    except:
        {'error'}, 400



@area_route.route("/v1/area/tax-param/delete", methods = ['POST'])
def DeleteArea():
    try:
        region_code = request.json['regione_code']
        regions = AreaTaxParam.query.filter(AreaTaxParam.city_id.equal(region_code)).all()
        if regions is None:
            return {'data is not exist'}, 400
        else:
            AreaTaxParam.query.filter_by(city_id=region_code).delete()
            db.session.commit()
            return {'done'}, 200
    except:
        {'error'}, 400



@area_route.route("/v1/area/tax-param/get", methods = ['GET'])
def GetTaxArea(id):
    try:
        data = list(map(lambda x: x.getDataArea(), AreaTaxParam.query.filter_by(id=id).all()))
        return data, 200
    except:
        {'error'}, 400


@area_route.route("/v1/area/tax-param/get", methods = ['GET'])
def GetTaxAreaAll(all):
    try:
        data = list(map(lambda x: x.getDataArea(), AreaTaxParam.query.all()))
        return data, 200
    except:
        {'error'}, 400



@area_route.route("/v1/area/tax/calc", methods = ['GET'])
def AreaTaxCalc(id, cadastr):
    try:
        data = list(map(lambda x: x.getDataArea(), AreaTaxParam.query.filter_by(id=id).all()))
        rate = int(data[2]) * int(cadastr)
        return rate, 200
    except:
        {'error'}, 400



