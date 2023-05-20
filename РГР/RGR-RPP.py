import requests,  json
import threading
import logging
import numpy    as np
import psycopg2 as pg

from aiogram                            import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state   import State, StatesGroup
from aiogram.dispatcher                 import FSMContext
from aiogram.types                      import ParseMode, KeyboardButton, ReplyKeyboardMarkup
from datetime                           import date, timedelta

API_KEY           = "61HMKMI43NOMJFEO"
ticker            = threading.Event()
WAIT_TIME_SECONDS = 60 * 60 * 24

TOKEN = "6165848339:AAE2sRqeBVZ7ss23Kw9J9zIx-0I7I5mWu5c"
logging.basicConfig(level = logging.INFO)

bot = Bot(token = TOKEN)
dp  = Dispatcher(bot, storage = MemoryStorage())

# Функция для подключения к базе данных
def connect_db():
    conn = pg.connect(user     = 'postgres',
                      password = 'postgres',
                      host     = 'localhost',
                      port     = '5432',
                      database = 'RGZ-RPP')
    return conn

def period_recalculate():
    while not ticker.wait(WAIT_TIME_SECONDS):
        recalculate_stocks()


async def add_stock_bd(user_id, stock_name):
    averages = get_values(stock_name)
    pg.cursor.execute("""select *
                           from stock
                     where user_id = %s
                       and stock_name = %s""",
                    (user_id, stock_name,))
    user = pg.cursor.fetchall()
    if len(user) == 0:
        pg.cursor.execute("""insert into stock (user_id, stock_name, averages)
                                  values (%s, %s, %s)""",
                                         (user_id, stock_name, averages,))
        pg.conn.commit()
        return f'Ценная бумага {stock_name} добавлена к отслеживаемым'
    else:
        pg.cursor.execute("""update stock
                                set averages   = %s
                              where user_id    = %s
                                and stock_name = %s""",
                                (averages, user_id, stock_name,))
        pg.conn.commit()
        return f'Ценная бумага {stock_name} обновлена'

def select_stocks(name):
    pg.cursor.execute("""select stock_name,
                                entry,
                                eject
                           from stock
                          where stock_name = %s""", (name,))
    stocks = pg.cursor.fetchall()
    msg    = ''
    for stock_name, entry, eject in stocks:
        if entry == 'null' or eject == 'null':
            msg += f'Для ценной бумаги {stock_name} не найдено значений :('
        else:
            msg += f'Акция {stock_name} имеет оптимальную точку входа: {entry} оптимальную точку выхода: {eject}'
    return msg


async def recalculate_stocks():
    pg.cursor.execute("""select * from stock""")
    stocks = pg.cursor.fetchall()
    for _, user_id, stock_name, entry, eject in stocks:
        averages = get_values(stock_name)
        pg.cursor.execute("""update stock
                                set averages   = %s
                              where user_id    = %s
                                and stock_name = %s""",
                                (averages, user_id, stock_name,))

# Создание списка кнопок
buttons = [
    [
        KeyboardButton(text = "Добавить ценную бумагу"),
        KeyboardButton(text = "Показатели ценных бумаг"),
        KeyboardButton(text = "Медиана цены закрытия"),
    ]
]

keyboard = ReplyKeyboardMarkup(
    keyboard          = buttons,
    resize_keyboard   = True,
    one_time_keyboard = True
)

class States(StatesGroup):
    add_security = State()


# Обработчик для команды /start
@dp.message_handler(commands = ['start'])
async def start_handler(message: types.Message):
    await message.answer("""Привет! Я бот для расчета ценных бумаг. Для начала, выбери действия ниже.
                            Действия должны быть в порядке:
                            1. /start,
                            2. Кнопка 'Добавить ценную бумагу',
                            3. Кнопка 'Показатели ценных бумаг',
                            4. Кнопка 'Медиана цены закрытия'!""")
    await message.answer("Выберите действие:", reply_markup = keyboard)


# Обработчик для команды /help
@dp.message_handler(commands = ['help'])
async def help_handler(message: types.Message):
    await message.answer("Нажал на /help?) А нужно было было нажимать на /start. Нажимай :)")


# Обработчик для команды "Добавить ценную бумагу к портфелю"
@dp.message_handler(lambda message: message.text == 'Добавить ценную бумагу')
async def add_security(message: types.Message):
    # Отправляем пользователю сообщение с просьбой ввести имя ценной бумаги
    await message.answer("Введите имя ценной бумаги:")
    await States.add_security.set()


# Обработчик для получения имени ценной бумаги после команды "Добавить ценную бумагу к портфелю"
@dp.message_handler(state=States.add_security)
async def save_security(message: types.Message, state: FSMContext):
    # Получаем имя ценной бумаги, введенное пользователем
    security_name = message.text

    # Сохраняем ценную бумагу в базе данных
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("insert into securities (user_id, security_name) values (%s, %s)",
                   (message.from_user.id, security_name))
    conn.commit()
    conn.close()

    await message.answer(f"Ценная бумага {security_name} добавлена к отслеживаемым в Базу Данных!", reply_markup = keyboard)
    await state.finish()


# Обработчик для команды "Показатели ценных бумаг"
@dp.message_handler(lambda message: message.text == 'Показатели ценных бумаг')
async def show_indicators(message: types.Message):
    msg = await select_stocks(message.text)
    await message.answer(msg)

def calculate_and_store_data(security_name):
    url      = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={security_name}&apikey={API_KEY}"
    response = requests.get(url)
    return json.loads(response.text)

def get_values(security_name):
    data = calculate_and_store_data(security_name)

    # Если компания не найдена, возвращаем налы
    if data.get('Error Message'):
        return 'null', 'null'
    
    # Дней в периоде
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
        day = (date.today() - timedelta(days = day_offset)).isoformat()
        day_info = data['Time Series (Daily)'].get(day)
        day_offset = day_offset + 1

        # Пропускаем день, если по нему нет данных
        if day_info is None:
            continue

        dates.append(day)

        # Достаем значение ценности бумаги
        val = float(day_info['4. close'])
        vals.append(val)
        total = total + val
        days_period = days_period + 1

        # Если до текущего момента была подсчитана сумма по следующим 30 дням,
        # добавляем среднее значение в массив avg и обнуляем соответствующие переменные
        if days_period == n:
            avg = round(total / n, 2)
            avgs.append(avg)
            days_period = 0
            total = 0

        days_counted = days_counted + 1

    # Переворачиваем массивы, так как заполняли их от текущей даты к прошлой
    vals.reverse()
    avgs.reverse()
    dates.reverse()

    return avgs


# Обработчик для команды "Медиана цены закрытия"
@dp.message_handler(lambda message: message.text == 'Медиана цены закрытия')
async def median_handler(message: types.Message):
    # Получаем данные и вычисляем медиану
    conn   = connect_db()
    cursor = conn.cursor()
    cursor.execute("select indicator_value from indicators")
    rows   = cursor.fetchall()
    conn.close()

    indicator_values = [row[0] for row in rows]
    median_price     = np.median(indicator_values)

    # Отправляем ответ
    response = f"Медианная цена закрытия за последние 30 дней: {median_price}"
    await message.answer(response, parse_mode = ParseMode.HTML)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)
    period_recalculate()