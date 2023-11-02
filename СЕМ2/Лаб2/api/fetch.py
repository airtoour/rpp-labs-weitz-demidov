from flask import Blueprint, request, jsonify
from dict  import dict
fetch = Blueprint('fetch', __name__)


@fetch.route('/v1/fetch/taxes', methods=['GET'])
def fetch_all():
    try:
        return jsonify({dict}), 200
    except Exception:
        return jsonify({'message': 'no_data_found'}), 400


@fetch.route('/v1/fetch/tax', methods=['GET'])
def fetch_region():
    region_code = request.args.get('region_code')

    if region_code not in dict:
        return jsonify({'error': f"Регион с кодом {region_code} не существует!"}), 400

    return jsonify({'tax_region': dict[region_code]})


@fetch.route("/v1/fetch/calc", methods=['GET'])
def fetch_calc(region_code, cadastral_value, quantity_month):
    try:
        tax_data = dict[region_code]
        year_tax = (float(tax_data) * float(cadastral_value) * float(quantity_month)) / 12
        return {'Сумма налога за год: ', year_tax}
    except Exception:
        if region_code not in dict:
            return jsonify({'error': f"Регион с кодом {region_code} не существует!"}), 400
