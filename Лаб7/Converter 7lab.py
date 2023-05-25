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


def check(name):
    cursor.execute("""select id
                        from currency_rate
                       where base_currency = %s""", (name,))
    data_id = cursor.fetchall()
    if data_id:
        return data_id[0][0]
    else:
        return None


def get(name, id):
    try:
        cursor.execute("""select rate
                            from currency_rate_value
                           where currency_rate_id = %s
                             and currency_code    = %s""", (id, name,))
        data_id = cursor.fetchall()
        if data_id:
            rate = float(re.sub(r"[^0-9.]", r"", str(data_id[0][0])))
            return rate
        else:
            return None
    except Exception as e:
        print(e)


@app.get("/convert")
def convert_get(baseCurrency: str, convertedCurrency: str, amount: float):
    try:
        baseCurrencyId = check(baseCurrency)
        if baseCurrencyId is None:
            raise HTTPException(status_code = 404, detail = "Base currency not found")

        convertedCurrencyRate = get(convertedCurrency, baseCurrencyId)
        if convertedCurrencyRate is None:
            raise HTTPException(status_code = 404, detail = "Converted currency not found")

        convertedAmount = convertedCurrencyRate * amount
        return {'converted': convertedAmount}
    except Exception as e:
        print(e)
        raise HTTPException(status_code = 500)


if __name__ == '__main__':
    uvicorn.run(app, port = 10609, host = 'localhost')
