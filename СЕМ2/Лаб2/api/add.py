from flask import Blueprint, request

add = Blueprint('add', __name__)

@add.route("/v1/add/tax", methods = ['POST'])
def add_tax():
    try:
        region_code = request.json['regionCode']
        tax_data = request.json['tax']

        if region_code not in dict:
            dict[region_code] = tax_data
            return {'data added'}

    except:
        return {'data not added'}, 400