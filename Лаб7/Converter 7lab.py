import uvicorn
import psycopg2 as pg
import re

from fastapi import FastAPI, HTTPException
 
app = FastAPI()  # Подключение метода для общения микросервиса по запросам

conn = pg.connect(user     = 'postgres',
                  password = 'postgres',
                  host     = 'localhost',
                  port     = '5432',
                  database = 'lab7rpp')
cursor = conn.cursor()


# Функция проверяющая наличее основной валюты в бд и возвращения её айди при наличии
def check(name):
    cursor.execute("""select id
                        from currency_rate
                       where base_currency = %s""", (name,))
    data_id = cursor.fetchall()
    id = data_id[0][0]
    print(id)
    return (id)


# Функция получающая данные по валюте в которую конвертируем, осуществляет поиск по названию валюты и айди основной валюты
def get(name, id):
    try:
        print(id, name)
        cursor.execute("""select rate
                            from currency_rate_value
                           where currency_rate_id = %s
                             and currency_code    = %s""", (id, name,))
        data_id = cursor.fetchall()
        print (data_id)
        data_id = float (re.sub(r"[^0-9.]", r"", str(data_id)))
        return (data_id)

    except Exception as e:
        print(e)


# Микросервис, который по запросу выдает получает данные из бота, обрабатывает их и возвращает в бота результат обработки
@app.get("/convert")
def convert_get(baseCurrency: str, convertedCurrency: str, sum: float):
    try:  # метод который в котором происходит попытка выполнения
        baseCurrency = int(check(baseCurrency))
        convertedCurrency = float(get(convertedCurrency, baseCurrency))
        if convertedCurrency != 0 and baseCurrency != 0:
            res = convertedCurrency * sum
            return {'converted': res}  # в случае успешного выполнения возвращает в бота результат конвертирования
    except Exception as e:             # в случае ошибки при выполнение основного тела выполняет следующее тело
        print(e)
        raise HTTPException(500)       # в случае ошибки при выполнение основного тела возвращается ответ 500


if __name__ == '__main__':
    uvicorn.run(app, port = 10609, host = 'localhost')
