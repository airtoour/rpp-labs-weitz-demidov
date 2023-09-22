from flask import Flask, request
import psycopg2 as pg

app = Flask(__name__)

# Функция для установления соединения с базой данных

conn = pg.connect(dbname   = "SEM1Lab",
                  user     = "postgres",
                  password = "postgres",
                  host     = "localhost",
                  port     = "5433"
)
cur = conn.cursor()

message_body = {}
error_body   = {}

# Задание 1:
    # Функция проверки наличия записи с заданным кодом региона
def select_region(id):
    try:
        cur.execute("select * from region where id = %s", (id,))
        existing_region = cur.fetchone()
        message_body = {'message': 'Запись найдена в таблице region!'}
        return message_body, 200

    except Exception:
        error_body = {'reason': 'Запись с таким регионом не найдена!'}
        if not existing_region:
            return error_body, 400

    # Функция вставки новой записи в таблицу region
def insert_region(id, name):
    try:
        cur.execute("""insert into region(id, name)
                            values (%s, %s)""", (id, name))
        conn.commit()
        conn.close()
        message_body = {'message': 'Запись с id региона успешно добавлена в таблицу region!'}
        return message_body, 200
    except Exception:
        error_body = {'reason': 'Запись с таким регионом уже существует в таблице region!'}
        return error_body, 400

    # Эндпоинт для добавления информации о регионе
@app.route('/v1/add/region', methods = ['POST'])
def add_region():
    try:
        # Извлекаем данные из тела запроса
        req  = request.json
        id   = req['id']
        name = req['name']

        # Выполняем вышенаписанный функционал
        result, status_code = select_region(id)
        result, status_code = insert_region(id, name)

        return result, status_code
    except Exception:
        return result, status_code


# Задание 2:
    # Функция выборки всей таблицы tax_param
def select_full_tax_param(id):
    try:
        cur.execute("select * from tax_param where id = %s", (id,))
        cur.fetchone()

        message_body = {'message': 'Таблица готова к использованию!'}

        return message_body, 200
    except Exception:
        error_body = {'reason': 'Таблица пуста или неправильные вводные данные :('}
        return error_body, 404

    # Функция проверки наличия записи с заданным идентификатором записи в таблице tax_param
def select_insert_tax_param(id, city_id, from_hp_car, to_hp_car, from_production_year_car, to_production_year_car, rate):
    try:
        result, status_code = select_region(city_id)
        result2, status_code2 = select_full_tax_param(id)

        if status_code and status_code2 != 200:
            cur.execute("""insert into tax_param(id, city_id, from_hp_car, to_hp_car, from_production_year_car, to_production_year_car, rate)
                                 values(%s,%s,%s,%s,%s,%s,%s)""",
                        (id, city_id, from_hp_car, to_hp_car, from_production_year_car, to_production_year_car, rate)
                        )
            conn.commit()

            message_body = {'message': 'Запись успешно добавлена в таблицу!'}
            return message_body, 200
        else:
            error_body = {'reason': 'Информация не найлена, или произошла техническая ошибка!'}
            return error_body, 404
        
        return result and result2, 200
    except Exception:
        if status_code or status_code2 != 200:
            return result, status_code

    # Эндпоинт для добавления объекта налогообложения
@app.route('/v1/add/tax-param', methods = ['POST'])
def add_tax_param():
    try:
        if 'id' not in request.json or 'city_id' not in request.json or 'from_hp_car' not in request.json or 'to_hp_car' not in request.json or 'from_production_year_car' not in request.json or 'to_production_year_car' not in request.json or 'rate' not in request.json:
            error_body = {'reason': 'Одно/несколько поле(й) пуст(ы)'}
            return error_body, 400

        # Извлекаем данные из тела запроса
        req                      = request.json
        city_id                  = req['city_id']
        from_hp_car              = req['from_hp_car']
        to_hp_car                = req['to_hp_car']
        from_production_year_car = req['from_production_year_car']
        to_production_year_car   = req['to_production_year_car']
        rate                     = req['rate']

        # Выполняем вышенаписанный функционал
        result, status_code = select_region(id)
        result, status_code = select_insert_tax_param(city_id, from_hp_car, to_hp_car, from_production_year_car,
                                               to_production_year_car, rate)

        if status_code != 201:
            return result, status_code

        return result, status_code
    except Exception:
        return error_body, 401

# Задание 3
    # Функция ппроверок и инсертов
def select_insert_auto(city_id, horse_power, production_year, name):
    cur.execute("select * from region where id = %s", (city_id))
    region_exist = cur.fetchone()

    try:
        if region_exist:
            cur.execute("""select id
                             from tax_param
                            where from_hp_car              <= %s
                              and to_hp_car                >= %s
                              and from_production_year_car <= %s
                              and to_production_year_car   >= %s""",
                        (horse_power, horse_power, production_year, production_year,)
                        )
            tax_exist = cur.fetchone()

            if tax_exist:
                # Если такой налог существует, селектии нужные данные и считаем сумму налога
                tax_id = int(tax_exist[0])
                cur.execute("select rate from tax_param where id = %s", (tax_id,))

                rate   = int(cur.fetchone()[0])
                tax    = rate * int(horse_power)

                # Инсертим данные в бд
                cur.execute("""insert into auto(city_id, tax_id, name, horse_power, production_year, tax) 
                                    values(%s,%s,%s,%s,%s,%s)""",
                            (city_id, tax_id, name, horse_power, production_year, tax)
                            )
                conn.commit()
                message_body = {'message': 'Сработало!'}
                return message_body, 202
            else:
                error_body = {'reason': 'Ошибка при работе функции!'}
                return error_body, 402
        else:
            error_body = {'reason': 'no_data_found'}
            return error_body, 404
    except Exception:
        error_body = {'reason': 'Техническая ошибка при работе функции!'}
        return error_body, 402

    # Эндпоинт для добавления автомобиля
@app.route('/v1/add/auto', methods = ['POST'])
def add_auto():
    try:
        # вытаскиваем данные из запроса
        req             = request.get_json()
        city_id         = req['city_id']
        name            = req['name']
        horse_power     = req['horse_power']
        production_year = req['production_year']

        result, status_code = select_insert_auto(city_id, horse_power, production_year, name)

        return result, status_code
    except Exception:
        if status_code != 202:
            return result, status_code

# Задание 4
    # Функция селекта из auto
def select_auto(id):
    try:
        cur.execute("select * from auto where id = %s", (int(id),))
        cur.fetchone()

        message_body = {'message': 'Запись найдена!'}
        return message_body, 200
    except Exception:
        error_body = {'reason': 'no_data_found'}
        return error_body, 404

    # Эндпоинт получения информации по всем автомобилям
@app.route('/v1/auto/<id>', methods=['GET'])
def auto(id):
    try:
        auto = select_auto(id)
        message_body = {"Auto": f"{auto}"}
        return message_body, 200
    except Exception:
        error_body = {'reason': 'Ошибка!'}
        return error_body, 400


if __name__ == '__main__':
    app.run(debug = True)