from flask import Blueprint

fetch = Blueprint('fetch', __name__)

@fetch.route("/v1/fetch/taxes", methods = ['GET'])
def fetch_all():
    try:
        return {dict}
    except:
        return {'data not exist'}, 400


@fetch.route("/v1/fetch/tax", methods=['GET'])
def fetch_region(region_code):
    try:
        return {dict[region_code]}
    except:
        return {'data not exist'}, 400


@fetch.route("/v1/fetch/calc", methods=['GET'])
def fetch_calc(region_code, cadastral_value, quantity_month):
    try:
        tax_data = dict[region_code]
        year_tax_data = (float(tax_data) * float(cadastral_value) * float(quantity_month)) / 12
        return {'Сумма налога за год: ', year_tax_data}
    except:
        return {'data not exist'}, 400