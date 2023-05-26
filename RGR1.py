import requests
import json
from datetime import date, timedelta
import threading
import psycopg2 as pg
from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message

ALPHAVANTAGE_API_KEY = '9OZBY4NHW13I3EK4'
API_TOKEN = '6165848339:AAE2sRqeBVZ7ss23Kw9J9zIx-0I7I5mWu5c'
WAIT_TIME_SECONDS = 60 * 60 * 24

conn = pg.connect(user='postgres', password='postgres', host='localhost', port='5432', database='RGZ_Sheav_Tim')
cursor = conn.cursor()


class Form(StatesGroup):
    save = State()
    show = State()


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

ticker = threading.Event()

def periodically_recalculate_stocks():
    while not ticker.wait(WAIT_TIME_SECONDS):
        recalculate_stocks()


async def add_stock_bd(user_id, stock_name):
    data = get_values_and_averages(stock_name)
    cursor.execute(
        f"""SELECT * FROM stock
        WHERE user_id = {user_id}
        AND stock_name = '{stock_name}'"""
    )
    users = cursor.fetchall()
    if len(users) == 0:
        cursor.execute(
            f"""INSERT INTO stock (user_id, stock_name, averages_open, averages_close, max_price, min_price)
             VALUES ({user_id}, '{stock_name}', '{data[0]}', '{data[1]}', '{data[2]}', '{data[3]}')"""
        )
        conn.commit()
        return f'Ценная бумага {stock_name} добавлена к отслеживаемым'
    else:
        cursor.execute(
            f"""UPDATE stock
            SET averages_open = '{data[0]}',
                averages_close = '{data[1]}',
                max_price = '{data[2]}',
                min_price = '{data[3]}'
            WHERE user_id = {user_id}
            AND stock_name = '{stock_name}'"""
        )
        conn.commit()
        return f'Ценная бумага {stock_name} обновлена'


def get_stocks_by_name(name):
    cursor.execute(
        f"""SELECT stock_name, averages_open, averages_close, max_price, min_price FROM stock
        WHERE stock_name = '{name}'"""
    )
    stocks = cursor.fetchall()
    msg = ''
    for stock_name, averages_open, averages_close, max_price, min_price in stocks:
        if any(value is None for value in (averages_open, averages_close, max_price, min_price)):
            msg += f'Для ценной бумаги {stock_name} не найдено значений\n\n'
        else:
            msg += f'Акция {stock_name} имеет\n' \
                   f'Cреднее значение открытия {averages_open}\n\n' \
                   f'Cреднее значение закрытия {averages_close}\n\n' \
                   f'Наибольшая цена бумаги {max_price}\n\n' \
                   f'Наименьшая цена бумаги {min_price}\n\n'
    return msg


async def recalculate_stocks():
    cursor.execute(
        f"""SELECT * FROM stock """
    )
    stocks = cursor.fetchall()
    for _, user_id, stock_name, _ in stocks:
        data = get_values_and_averages(stock_name)
        cursor.execute(
            f"""UPDATE stock
            SET averages_open = '{data[0]}',
                averages_close = '{data[1]}',
                max_price = '{data[2]}',
                min_price = '{data[3]}'
            WHERE user_id = {user_id} AND stock_name = '{stock_name}'"""
        )
        conn.commit()


def fetch_data(company_symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={company_symbol}&apikey={ALPHAVANTAGE_API_KEY}"
    response = requests.get(url)
    return json.loads(response.text)


def get_values_and_averages(company_symbol):
    data = fetch_data(company_symbol)
    n = 30
    day_offset = 0
    days_counted = 0
    val1 = 0.0
    val2 = 0.0
    min_val = 1000.0
    max_val = 0.0

    while day_offset < n:
        day = (date.today() - timedelta(days=day_offset)).isoformat()
        day_info = data['Time Series (Daily)'].get(day)
        day_offset += 1

        if day_info is None:
            continue

        val1 += float(day_info['1. open'])
        val_max = float(day_info['2. high'])
        val_min = float(day_info['3. low'])
        val2 += float(day_info['4. close'])

        if max_val < val_max:
            max_val = val_max

        if min_val > val_min:
            min_val = val_min

    avg_open = val1 / n
    avg_close = val2 / n

    return avg_open, avg_close, max_val, min_val


@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    kb = ReplyKeyboardMarkup(is_persistent=True, resize_keyboard=True, row_width=1)
    kb.add(KeyboardButton('/Add'))
    kb.add(KeyboardButton('/Show'))

    await message.answer(text='Добро пожаловать в чат бот!', reply_markup=kb)


@dp.message_handler(commands=['Add'])
async def add_stock(message: Message):
    await message.answer('Введите имя ценной бумаги')
    await Form.save.set()


@dp.message_handler(state=Form.save)
async def save_stock(message: Message, state: FSMContext):
    ide = message.from_user.id
    stock_name = message.text
    msg = await add_stock_bd(ide, stock_name)
    await message.answer(msg)
    await state.finish()


@dp.message_handler(commands=['Show'])
async def stock_get(message: Message):
    await message.answer('Введите название ценной валюты')
    await Form.show.set()


@dp.message_handler(state=Form.show)
async def show_stock(message: Message, state: FSMContext):
    msg = get_stocks_by_name(message.text)
    await message.answer(msg)
    await state.finish()


if __name__ == '__main__':
    threading.Thread(target=periodically_recalculate_stocks).start()
    executor.start_polling(dp, skip_updates=True)