from flask import Blueprint, request
from Config import db

regions = Blueprint('regions',__name__)


class Region(db.Model):
    id = db.Column(db.Serial, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    def getData(self):
        return f'<Region ID: {self.id}; Region name: {self.name}>'


class CarTaxParam(db.Model):
    id = db.Column(db.Serial, primary_key=True)
    city_id = db.Column(db.Integer, ForeignKey('region.id'))
    from_hp_car = db.Column(db.Integer, nullable = False)
    to_hp_car = db.Column(db.Integer, nullable = False)
    from_production_year_car = db.Column(db.Integer, nullable = False)
    to_production_year_car = db.Column(db.Integer, nullable = False)
    rate = db.Column(db.Numeric, nullable = False)

    def getDataCar(self):
        return f'< Tax ID: {self.id}; ' \
               f'City ID {self.city_id}; ' \
               f'From HP car: {self.from_hp_car}; ' \
               f'To HP car: {self.to_hp_car}; ' \
               f'From production year car {self.from_production_year_car}; ' \
               f'To production year car: {self.to_production_year_car};' \
               f'Rate: {self.rate} > '



class AreaTaxParam(db.Model):
    id = db.Column(db.Serial, primary_key=True)
    city_id = db.Column(db.Integer, ForeignKey('Region.id'))
    rate = db.Column(db.Numeric, nullable=False)

    def getDataArea(self):
        return f'<Tax ID: {self.id}; Region ID: {self.city_id}; Rate: {self.rate}>'




@regions.route("/v1/region/add", methods = ['POST'])
def AddRegion():
    try:
        region_code = request.json['regione_code']
        region_name = request.json['region_name']
        regions = Region.query.filter(Region.id.equal(region_code)).all()
        if regions is None:
            region = Region(name = region_name)
            code = Region(id = region_code)
            db.session.add(region)
            db.session.add(code)
            db.session.commit()
            return {'done'}, 200
        else:
            return {'data exist'}, 400
    except:
        {'error'}, 400


@regions.route("/v1/region/update", methods = ['POST'])
def UpdateRegion():
    try:
        region_code = request.json['regione_code']
        region_name = request.json['region_name']
        regions = Region.query.filter(Region.id.equal(region_code)).all()
        if regions is None:
            return {'data is not exist'}, 400
        else:
            Region.query.filter_by(id=region_code).update({'name': region_name})
            CarTaxParam.query.filter_by(city_id=region_code).update({'name': region_name})
            AreaTaxParam.query.filter_by(city_id=region_code).update({'name': region_name})
            db.session.commit()
            return {'done'}, 200
    except:
        {'error'}, 400



@regions.route("/v1/region/delete", methods = ['POST'])
def DeleteRegion():
    try:
        region_code = request.json['regione_code']
        regions = Region.query.filter(Region.id.equal(region_code)).all()
        if regions is None:
            return {'data is not exist'}, 400
        else:
            Region.query.filter_by(id=region_code).delete()
            CarTaxParam.query.filter_by(city_id=region_code).delete()
            AreaTaxParam.query.filter_by(city_id=region_code).delete()
            db.session.commit()
            return {'done'}, 200
    except:
        {'error'}, 400




@regions.route("/v1/region/get", methods = ['GET'])
def GetRegion(id):
    try:
        region = list(map(lambda x: x.getData(), Region.query.filter_by(id=id).all()))
        return region, 200
    except:
        {'error'}, 400



@regions.route("/v1/region/get/all", methods = ['GET'])
def GetRegionAll(all):
    try:
        region = list(map(lambda x: x.getData(), Region.query.all()))
        return region, 200
    except:
        {'error'}, 400