import requests, json
import threading, time
import logging
import numpy as np
import psycopg2 as pg

from aiogram                            import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state   import State, StatesGroup
from aiogram.dispatcher                 import FSMContext
from aiogram.types                      import ParseMode

API_KEY = "61HMKMI43NOMJFEO"
TOKEN = "6165848339:AAE2sRqeBVZ7ss23Kw9J9zIx-0I7I5mWu5c"
logging.basicConfig(level = logging.INFO)

bot = Bot(token = TOKEN)
dp = Dispatcher(bot, storage = MemoryStorage())

# Создание списка кнопок
buttons = [
    types.InlineKeyboardButton(text = 'Добавить ценную бумагу',  callback_data = 'add_security'),
    types.InlineKeyboardButton(text = 'Показатели ценных бумаг', callback_data = 'save_cur'),
    types.InlineKeyboardButton(text = 'Медиана цены закрытия',   callback_data = 'median')
]

# Создание объекта класса InlineKeyboardMarkup с передачей списка кнопок в конструктор
keyboard = types.InlineKeyboardMarkup(row_width = 3)
keyboard.add(*buttons)


# Функция для подключения к базе данных
def connect_db():
    conn = pg.connect(user     = 'postgres',
                      password = 'postgres',
                      host     = 'localhost',
                      port     = '5432',
                      database = 'RGZ-RPP')
    return conn

class States(StatesGroup):
    add_security = State()


# Обработчик для команды /start
@dp.message_handler(commands = ['start'])
async def start_handler(message: types.Message):
    await message.answer(f"""Привет! Я бот для расчета ценных бумаг. Для начала, выбери действия ниже.
                             Действия должны быть в порядке:
                             /start,
                             Кнопка 'Добавить ценную бумагу',
                             Кнопка 'Показатели ценных бумаг',
                             Кнопка 'Медиана цены закрытия'!
                          """)
    await message.answer("Выберите действие:", reply_markup = keyboard)


# Обработчик для команды /help
@dp.message_handler(commands = ['help'])
async def help_handler(message: types.Message):
    await message.answer("Нажал на /help?) А нужно было было нажимать на /start. Нажимай :)")


# Обработчик для команды "Добавить ценную бумагу к портфелю"
@dp.message_handler(lambda c: c.data == 'add_security')
async def add_security(message: types.Message):

    # Отправляем пользователю сообщение с просьбой ввести имя ценной бумаги
    await message.reply("Введите имя ценной бумаги:")

    # Сохраняем состояние пользователя в хранилище FSM
    await States.add_security.set()

# Обработчик для получения имени ценной бумаги после команды "Добавить ценную бумагу к портфелю"
@dp.message_handler(state = States.add_security)
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


# Обработчик для Индикаторов
@dp.message_handler(lambda c: c.data == 'show_indicators')
async def show_indicators(message: types.Message):
    # Получаем показатели из базы данных для данного пользователя
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("select security_name from securities where user_id = %s", (message.from_user.id,))
    securities = cursor.fetchall()
    conn.close()

    if securities:
        # Обрабатываем каждую ценную бумагу
        for security in securities:
            security_name = security[0]
            # Получаем показатели для ценной бумаги из базы данных
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("select indicator_value from indicators where security_name = %s",
                           (security_name,))
            indicators = cursor.fetchall()
            conn.close()

            if indicators:
                # Отправляем показатели пользователю
                await message.answer(f"Показатели для ценной бумаги {security_name}:", reply_markup = keyboard)
                for indicator in indicators:
                    await message.answer(f"- {indicator[0]}")
            else:
                await message.answer(f"Для ценной бумаги {security_name} не найдено значений!")
    else:
        await message.answer("У вас нет отслеживаемых ценных бумаг :( Проверьте их наличие в Базе данных!")


# Определение показателя доходности ценной бумаги
def avg_close_sum(security_name):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={security_name}&apikey={API_KEY}"
    response = requests.get(url)
    data = json.loads(response.text)

    series = data['Time Series (Daily)']
    close_prices = []

    for date, values in series.items():
        close_price = float(values['4. close'])
        close_prices.append(close_price)

    returns = np.diff(close_prices)/close_prices[:-1]
    indicator_value = np.mean(returns)

    return indicator_value

def task():
    blanks = []
    while True:
        for blank in blanks:
            avg_close_sum(blank)

            ts = time.time()
            # Store the time value in the database
        time.sleep(10)

# Start the task
task()

def calculate_indicators_task():
    while True:
        # Получаем список ценных бумаг из базы данных
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("select security_name from securities")
        securities = cursor.fetchall()
        conn.close()

        if securities:
            for security in securities:
                security_name = security[0]

                # Вызываем функцию для расчета показателя доходности
                indicator_value = avg_close_sum(security_name)

                # Сохраняем показатель доходности в базу данных
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("insert into indicators (security_name, indicator_value) values (%s, %s)",
                               (security_name, indicator_value,))
                conn.commit()
                conn.close()

        # Приостанавливаем выполнение на 1 день
        time.sleep(24 * 60 * 60)

@dp.message_handler(lambda c: c.data == 'median')
async def median_handler(message: types.Message):
    
    
    # загрузка данных и вычисление медианы
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("select indicator_value from indicators")
    rows = cursor.fetchall()
    conn.close()

    df = np.array(rows)
    close_prices = df['Close'][-30:]
    median_price = np.median(close_prices)
    
    # отправка ответа
    response = f"Медианная цена закрытия за последние 30 дней: {median_price}"
    await message.answer(message.chat.id, response, parse_mode = ParseMode.HTML)

if __name__ == '__main__':
    thread = threading.Thread(target = task)
    # Запускаем экземпляр 'thread'
    executor.start_polling(dp, skip_updates = True)