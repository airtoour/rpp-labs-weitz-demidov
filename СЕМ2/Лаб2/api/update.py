from flask import Blueprint, request

update = Blueprint('update', __name__)

@update.route("/v1/update/tax ", methods = ['POST'])
def update_tax():
    try:
        region_code = request.json['regionCode']
        tax_data = request.json['tax']
        dict.update(region_code, tax_data)

        return {dict[region_code]}

    except Exception:
        return {'data not exist'}, 400