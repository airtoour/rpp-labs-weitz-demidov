from flask import Blueprint, request, jsonify

add = Blueprint('add', __name__)


@add.route('/v1/add/tax', methods=['POST'])
def add_tax():
    req = request.get_json()
    region_code = req.get('region_code')
    tax_rate = req.get('tax_rate')

    try:
        dict[region_code] = tax_rate
        return jsonify({'message': f"Налоговая ставка в количестве {tax_rate} успешно добавлена!"}), 200
    except Exception:
        if region_code in dict:
            return jsonify({"message": f"Регион с кодом {region_code} уже существует!"}), 400
