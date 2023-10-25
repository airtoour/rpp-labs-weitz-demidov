from flask import Blueprint, request, jsonify

update = Blueprint('update', __name__)


@update.route('/v1/update/tax', methods=['POST'])
def update_tax():
    req = request.get_json()
    region_code = req.get('region_code')
    new_tax = req.get('tax')

    try:
        if region_code in dict:
            dict.update(region_code, new_tax)
            return jsonify({'message': f"Налоговая ставка в количестве {new_tax} успешно обновлена!"}), 200
    except Exception:
        return jsonify({'error': f"Регион с кодом {region_code} не существует!"}), 400
