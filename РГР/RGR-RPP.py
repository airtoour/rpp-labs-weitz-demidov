import requests
import json
import os
import threading

import psycopg2 as pg
from datetime import date, timedelta

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message

ALPHAVANTAGE_API_KEY = '9OZBY4NHW13I3EK4'
# Токен бота
API_TOKEN = '6165848339:AAE2sRqeBVZ7ss23Kw9J9zIx-0I7I5mWu5c'
# Таймер для перерасчета показателей акций (24 часа)
WAIT_TIME_SECONDS = 60 * 60 * 24
# Конфиг для локальной БД
conn = pg.connect(user='postgres', password='postgres', host='localhost', port='5432', database='RGZ-RPP')
cursor = conn.cursor()


class Form(StatesGroup):
    save = State()


ticker = threading.Event()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


# Раз в WAIT_TIME_SECONDS секунд пересчитываем показатели для всех бумаг
def periodically_recalculate_stocks():
    while not ticker.wait(WAIT_TIME_SECONDS):
        recalculate_stocks()


async def add_stock_bd(user_id, stock_name):
    averages = get_values_and_averages(stock_name)
    cursor.execute(
        f"""SELECT * FROM stock
        WHERE user_id = {user_id}
        AND stock_name = '{stock_name}'"""
    )
    users = cursor.fetchall()
    if len(users) == 0:
        cursor.execute(
            f"""INSERT INTO stock (user_id, stock_name, averages)
             VALUES ({user_id}, '{stock_name}', '{averages}')"""
        )
        conn.commit()
        return f'Ценная бумага {stock_name} добавлена к отслеживаемым'
    else:
        cursor.execute(
            f"""UPDATE stock
            SET averages = '{averages}'
            WHERE user_id = {user_id}
            AND stock_name = '{stock_name}'"""
        )
        conn.commit()
        return f'Ценная бумага {stock_name} обновлена'


def get_stocks_by_name(name):
    cursor.execute(
        f"""SELECT stock_name, entry, eject FROM stock
        WHERE stock_name = '{name}'"""
    )
    stocks = cursor.fetchall()
    msg = ''
    for stock_name, entry, eject in stocks:
        if entry == 'null' or eject == 'null':
            msg += f'Для ценной бумаги {stock_name} не найдено значений\n\n'
        else:
            msg += f'Акция {stock_name} имеет\nоптимальную точку входа: {entry}\nоптимальную точку выхода: {eject}\n\n'
    return msg


async def recalculate_stocks():
    cursor.execute(
        f"""SELECT * FROM stock """
    )
    stocks = cursor.fetchall()
    for _, user_id, stock_name, entry, eject in stocks:
        averages = get_values_and_averages(stock_name)
        cursor.execute(
            f"""UPDATE stock
            SET averages = '{averages}'
            WHERE user_id = {user_id} AND stock_name = '{stock_name}'"""
        )


@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    kb = ReplyKeyboardMarkup(is_persistent=True, resize_keyboard=True, row_width=1)
    kb.add(KeyboardButton('Добавить ценную бумагу к портфелю'))
    kb.add(KeyboardButton('Показатели отслеживаемых ценных бумаг'))

    await message.answer(text='Добро пожаловать в чат бот!', reply_markup=kb)


@dp.message_handler(text='Добавить ценную бумагу к портфелю')
async def add_stock(message: Message):
    await message.answer('Введите имя ценной бумаги')
    await Form.save.set()


@dp.message_handler(state=Form.save)
async def save_stock(message: Message, state: FSMContext):
    ide=message.from_id
    print(ide)
    test=message.text
    print(test)
    msg = await add_stock_bd(ide, test)
    await message.answer(msg)
    await state.finish()


@dp.message_handler(text='Показатели отслеживаемых ценных бумаг')
async def echo(message: Message):
    msg = await get_stocks_by_name(message.text)
    await message.answer(msg)


def fetch_data(company_symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={company_symbol}&apikey={ALPHAVANTAGE_API_KEY}"
    response = requests.get(url)
    return json.loads(response.text)


def get_values_and_averages(company_symbol):
    data = fetch_data(company_symbol)

    # Если компания не найдена, возвращаем налы
    if data.get('Error Message'):
        return 'null', 'null'

    maximum_days = 30
    # Длина периода для рассчета среднего
    n = 30
    # Сумма ценностей в текущий период
    total = 0
    # Счетчик дней в текущий период
    days_period = 0
    # Счетчик отступа дней от сегодня
    day_offset = 0
    # Счетчик дней, для которых удалось получить данные
    days_counted = 0
    # Здесь храним значения по дням
    vals = []
    # Массив с датами
    dates = []
    # Здесь храним средние значения по периодам длиной n
    avgs = []

    while days_counted < maximum_days:
        day = (date.today() - timedelta(days=day_offset)).isoformat()
        day_info = data['Time Series (Daily)'].get(day)
        day_offset += 1

        # Пропускаем день, если по нему нет данных
        if day_info is None:
            continue

        dates.append(day)

        # Достаем значение ценности бумаги
        val = float(day_info['4. close'])
        vals.append(val)
        total += val
        days_period += 1

        # Если до текущего момента была подсчитана сумма по следующим 30 дням,
        # добавляем среднее значение в массив avg и обнуляем соответствующие переменные
        if days_period == n:
            avg = round(total / n, 2)
            avgs.append(avg)
            days_period = 0
            total = 0

        days_counted += 1

    # Переворачиваем массивы, так как заполняли их от текущей даты к прошлой
    vals.reverse()
    avgs.reverse()
    dates.reverse()

    return avgs


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    periodically_recalculate_stocks()
