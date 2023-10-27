from flask import Flask, request, jsonify
import psycopg2 as pg

app = Flask(__name__)

# Функция для установления соединения с базой данных
conn = pg.connect(dbname   = "S2LR1",
                  user     = "postgres",
                  password = "postgres",
                  host     = "localhost",
                  port     = "5433"
                  )
cur = conn.cursor()


# Задание 1:
# Эндпоинт для добавления информации о регионе
@app.route('/v1/add/region', methods=['POST'])
def add_region():
    # Извлекаем данные из тела запроса
    req       = request.json
    city_id   = req['id']
    city_name = req['name']

    # Проверяем данные на наличие в таблице region
    cur.execute("select * from region where id = %s", (city_id,))
    region_exists = cur.fetchone()

    if region_exists:
        return jsonify({'message': f"id региона: ' {city_id} '  уже существует в таблице region!"}), 400
    else:
        try:
            # Инсёртим данные в таблицу region
            cur.execute("insert into region(id, name) values (%s, %s)", (city_id, city_name))
            conn.commit()
            conn.close()

            return jsonify({'message': f"Запись с id региона: {city_id} успешно добавлена в таблицу region!"}), 200
        except Exception:
            return jsonify({'error': f"Запись с id региона: {city_id} уже существует в таблице region!"}), 400



# Задание 2:
# Эндпоинт для добавления объекта налогообложения
@app.route('/v1/add/tax-param', methods=['POST'])
def add_tax_param():
    # Извлекаем данные из тела запроса
    req                      = request.json
    id_req                   = req['id']
    city_id                  = req['city_id']
    from_hp_car              = req['from_hp_car']
    to_hp_car                = req['to_hp_car']
    from_production_year_car = req['from_production_year_car']
    to_production_year_car   = req['to_production_year_car']
    rate_amount              = req['rate']

    # Проверяем данные на наличие в таблице tax_param
    cur.execute("select * from tax_param where city_id = %s", (city_id,))
    tax_exists = cur.fetchone()

    # Проверяем данные на наличие в таблице region
    cur.execute("select * from region where id = %s", (city_id,))
    region_exists = cur.fetchone()

    if not region_exists:
        return jsonify({'error': f"Регион {city_id} не найден в таблице region"}), 400

    if tax_exists:
        return jsonify({'error': f"Регион {city_id} уже существует в таблице tax_param"}), 400
    else:
        cur.execute("""insert into tax_param(id, city_id, from_hp_car, to_hp_car, from_production_year_car,
                                             to_production_year_car, rate)
                                      values(%s, %s, %s, %s, %s, %s, %s)""",
                    (id_req, city_id, from_hp_car, to_hp_car,
                     from_production_year_car, to_production_year_car, rate_amount))
        conn.commit()

        return jsonify({'message': 'Запись успешно добавлена в таблицу!'}), 200


# Задание 3
# Эндпоинт для добавления автомобиля
@app.route('/v1/add/auto', methods=['POST'])
def add_auto():
    req             = request.get_json()
    id_req          = req['id']
    city_id         = req['city_id']
    tax_id          = req['tax_id']
    name            = req['name']
    horse_power     = req['horse_power']
    production_year = req['production_year']

    # Проверяем данные на наличие в таблице region
    cur.execute("select * from region where id = %s", (city_id,))
    region_exists = cur.fetchone()

    if not region_exists:
        return jsonify({'error': f"Регион с кодом {city_id} не найден в таблице region"}), 400

    # Проверка наличия налогообложения
    cur.execute("select * from tax_param where id = %s", (tax_id,))
    tax_exists = cur.fetchone()

    if not tax_exists:
        return jsonify({'error': f"Налогообложение с id {tax_id} не найдено"}), 400

    # Вычисление налога
    tax = horse_power * tax_exists[6]

    # Сохранение данных в таблицу auto
    cur.execute("""insert into auto(id, city_id, tax_id, name, horse_power, production_year, tax)
                    values (%s, %s, %s, %s, %s, %s, %s)""", (id_req, city_id, tax_id, name, horse_power,
                                                             production_year, tax))
    conn.commit()
    return jsonify({'message': f"Автомобиль {name} успешно добавлен"}), 200


# Задание 4
# Эндпоинт получения информации по всем автомобилям
@app.route('/v1/auto/<id>', methods = ['GET'])
def auto(auto_id):
    try:
        cur.execute("select * from auto where id = %s", (auto_id,))
        auto_data = cur.fetchone()

        if auto_data:
            return jsonify({"message": f"{auto_data}"}), 200
        else:
            return jsonify({"message": "no_data_found"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 400


# Обработчик запроса на главную страницу
@app.route('/')
def home():
    return 'Главная страница!'


if __name__ == '__main__':
    app.run(debug = True)
