import requests
import json
import threading

import psycopg2 as pg
from datetime import date, timedelta

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message

API_KEY = '9OZBY4NHW13I3EK4'
# Токен бота
API_TOKEN = '6165848339:AAE2sRqeBVZ7ss23Kw9J9zIx-0I7I5mWu5c'
# Таймер для перерасчета показателей акций (24 часа)
WAIT_TIME_SECONDS = 60 * 60 * 24
# Конфиг для локальной БД
conn = pg.connect(user='postgres', password='postgres', host='localhost', port='5432', database='RGZ-RPP')
cursor = conn.cursor()


class Form(StatesGroup):
    save = State()
    show = State()


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


# Раз в WAIT_TIME_SECONDS секунд пересчитываем показатели для всех бумаг
def periodically_recalculate_stocks():
    ticker = threading.Event()
    while not ticker.wait(1):
        print("asd")
        recalculate_stocks()


async def add_stock_bd(user_id, stock_name):
    averages = get_values_and_averages(stock_name)
    cursor.execute(f"""select *
                         from stock
                        where user_id    = {user_id}
                          and stock_name = '{stock_name}'""")
    users = cursor.fetchall()
    if len(users) == 0:
        cursor.execute(f"""insert into stock (user_id, stock_name, averages)
                                values ({user_id}, '{stock_name}', '{averages}')""")
        conn.commit()
        return f'Ценная бумага {stock_name} добавлена к отслеживаемым'
    else:
        cursor.execute(
            f"""update stock
                   set averages   = '{averages}'
                 where user_id    = {user_id}
                   and stock_name = '{stock_name}'"""
        )
        conn.commit()
        return f'Ценная бумага {stock_name} обновлена'


def recalculate_stocks():
    cursor.execute(f"""select * from stock """)
    stocks = cursor.fetchall()
    for _, user_id, stock_name, averages in stocks:
        averages = get_values_and_averages(stock_name)
        cursor.execute(f"""update stock
                              set averages   = '{averages}'
                            where user_id    = {user_id}
                              and stock_name = '{stock_name}'""")


@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    keyboard = ReplyKeyboardMarkup(is_persistent=True, resize_keyboard=True, row_width=1)
    keyboard.add(KeyboardButton('Добавить ценную бумагу к портфелю'))
    keyboard.add(KeyboardButton('Показатели отслеживаемых ценных бумаг'))

    await message.answer(
        text='Привет, я Бот, который умеет работать с ценными бумагами. Нажми на кнопку на квлавиаутре!',
        reply_markup=keyboard)


@dp.message_handler(text='Добавить ценную бумагу к портфелю')
async def add_stock(message: Message):
    await message.answer('Введите имя ценной бумаги:')
    await Form.save.set()


@dp.message_handler(state=Form.save)
async def save_stock(message: Message, state: FSMContext):
    admin_id = message.from_id
    cost_paper = message.text
    msg = await add_stock_bd(admin_id, cost_paper)
    await message.answer(msg)

    keyboard = ReplyKeyboardMarkup(is_persistent=True, resize_keyboard=True, row_width=1)
    keyboard.add(KeyboardButton('Добавить ценную бумагу к портфелю'))
    keyboard.add(KeyboardButton('Показатели отслеживаемых ценных бумаг'))

    await message.answer(text='Выбери следующий метод:', reply_markup=keyboard)

    await state.finish()


@dp.message_handler(content_types=types.ContentType.TEXT, text='Показатели отслеживаемых ценных бумаг')
async def echo(message: Message):
    await message.answer("Введите название ценной бумаги:")
    await Form.show.set()


@dp.message_handler(state=Form.show)
async def show_work(message: Message):
    cursor.execute(f"""select stock_name,
                              averages
                         from stock
                        where stock_name = '{message.text}'""")
    stocks = cursor.fetchall()
    for stock_name, averages in stocks:
        if averages == 'null':
            await message.answer(f'Для ценной бумаги {stock_name} не найдено значений')
        else:
            avg_values = eval(averages)
            await message.answer(f'Акция {stock_name} имеет среднее значение: {avg_values[0]}')
    await State.finish()


def fetch_data(company_symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={company_symbol}&apikey={API_KEY}"
    response = requests.get(url)
    return json.loads(response.text)


def get_values_and_averages(company_symbol):
    data = fetch_data(company_symbol)

    # Если компания не найдена, возвращаем налы
    if data.get('Error Message'):
        return 'null', 'null'

    max_cnt_days = 30
    # Длина периода для рассчета среднего
    n = 30
    # Сумма ценностей в текущий период
    total = 0
    # Счетчик дней в текущий период
    period_days = 0
    # Счетчик отступа дней от сегодня
    skip_days = 0
    # Счетчик дней, для которых удалось получить данные
    days_counted = 0
    # Здесь храним значения по дням
    vals = []
    # Массив с датами
    dates = []
    # Здесь храним средние значения по периодам длиной n
    avgs = []

    while days_counted < max_cnt_days:
        day = (date.today() - timedelta(days=skip_days)).isoformat()
        day_info = data['Time Series (Daily)'].get(day)
        skip_days = skip_days + 1

        # Пропускаем день, если по нему нет данных
        if day_info is None:
            continue

        dates.append(day)

        # Достаем значение ценности бумаги
        val = float(day_info['4. close'])
        vals.append(val)
        total = total + val
        period_days = period_days + 1

        # Если до текущего момента была подсчитана сумма по следующим 30 дням,
        # добавляем среднее значение в массив avg и обнуляем соответствующие переменные
        if period_days == n:
            avg = round(total / n, 2)
            avgs.append(avg)
            period_days = 0
            total = 0

        days_counted = days_counted + 1

    # Разворачиваем массивы, для корректности
    vals.reverse()
    avgs.reverse()
    dates.reverse()

    return avgs


if __name__ == '__main__':
    thread = threading.Thread(target=periodically_recalculate_stocks)
    thread.start()
    executor.start_polling(dp, skip_updates=True)