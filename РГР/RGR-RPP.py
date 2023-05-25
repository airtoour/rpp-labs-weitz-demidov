import asyncio
import requests
import json
import threading
import aiogram
import numpy    as np
import psycopg2 as pg

from aiogram                            import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_KEY           = "61HMKMI43NOMJFEO"
TOKEN             = "6165848339:AAE2sRqeBVZ7ss23Kw9J9zIx-0I7I5mWu5c"
WAIT_TIME_SECONDS = 300

ticker = threading.Event()

# Создание бота и диспетчера
bot = Bot(token = TOKEN)
dp = Dispatcher(bot, storage = MemoryStorage())

# Подключение к базе данных Postgres
conn = pg.connect(database = "RGZ-RPP",
                  user     = "postgres",
                  password = "postgres",
                  host     = "localhost",
                  port     = "5432")
cur = conn.cursor()

# Функция для получения данных из API
def get_stock_data(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={API_KEY}"
    response = requests.get(url)
    data = json.loads(response.text)
    return data

# Функция расчета медианного значения цены закрытия за период анализа
def calculate_median(data):
    close_prices = []
    time_series = data["Time Series (Daily)"]
    for date, values in time_series.items():
        close_prices.append(float(values["4. close"]))
    median = np.median(close_prices)
    return median

# Функция обработки команды "Добавить ценную бумагу к портфелю"
async def add_stock(message: types.Message):
    await message.answer("Введите имя ценной бумаги")
    # Ожидание ответа пользователя с именем ценной бумаги
    response = await bot.wait_for("message")
    stock_name = response.text

    # Сохранение ценной бумаги в базе данных
    cur.execute("insert into securities(security_name) values (%s)", (stock_name,))
    conn.commit()

    await message.answer(f"Ценная бумага {stock_name} добавлена к отслеживаемым!")

# Функция обработки команды "Показатели отслеживаемых ценных бумаг"
async def show_indicators(message: types.Message):
    cur.execute("select security_name from securities")
    securities = cur.fetchall()

    for security in securities:
        stock_name = security[0]
        data = get_stock_data(stock_name)
        if "Time Series (Daily)" in data:
            median = calculate_median(data)
            await message.answer(f"Ценная бумага: {stock_name}, Медианное значение: {median}")
        else:
            await message.answer(f"Для ценной бумаги {stock_name} не найдено значений :(")

# Функция определения и сохранения показателя доходности ценной бумаги
def calculate_and_store_data():
    cur.execute("select security_name from securities")
    securities = cur.fetchall()

    for security in securities:
        stock_name = security[0]
        data = get_stock_data(stock_name)
        if "Time Series (Daily)" in data:
            median = calculate_median(data)
            cur.execute("insert into indicators(security_name, indicator_value) values (%s, %s)", (stock_name, median))
            conn.commit()

# Регистрация обработчиков команд
dp.register_message_handler(add_stock,       commands = "add_stock")
dp.register_message_handler(show_indicators, commands = "show_indicators")

# Запуск периодической задачи для расчета показателя доходности
def periodic_task():
    while not ticker.wait(WAIT_TIME_SECONDS):
        calculate_and_store_data()

# Запуск бота и периодической задачи
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(periodic_task())
    aiogram.executor.start_polling(dp, loop=loop)