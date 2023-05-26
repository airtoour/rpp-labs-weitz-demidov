import logging
import os
import psycopg2 as pg
import re
import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import BotCommand, BotCommandScopeDefault

TOKEN = "6165848339:AAE2sRqeBVZ7ss23Kw9J9zIx-0I7I5mWu5c"
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

conn = pg.connect(user='postgres',
                  password='postgres',
                  host='localhost',
                  port='5432',
                  database='lab7rpp')
cursor = conn.cursor()


# Обявление состояний для работы бота
class Form(StatesGroup):
    check = State()
    num = State()
    con = State()
    save_base = State()
    save_converted = State()
    save_converted_rate = State()
    save = State()


user_commands = [
    BotCommand(command='/start', description='start'),
    BotCommand(command='/convert', description='Конвертировать')
]

admin_commands = [
    BotCommand(command='/start', description='start'),
    BotCommand(command='/manage_currency', description='Менеджер валют'),
    BotCommand(command='/convert', description='Конвертировать')
]

param = {}  # Обявление словаря


# Функция для проверки айди администратора в бд
def get_from_admin():
    cursor.execute("""select chat_id
                        from admin
                       where id = 1""")
    admin_id = cursor.fetchone()
    return admin_id[0] if admin_id else None


ADMIN_ID = str(get_from_admin())


# функция выполняемая по команде из бота
@dp.message_handler(commands=['start'])
async def start_name_process(message: types.Message):
    await message.answer("""Привет! Я бот для конвертации валюты. Для начала, выбери обозначение валюты с помощью действия ниже.
                            Вот какие команды я знаю:
                            Введи /manage_currency - Управлять валютами""")


# функция выполняемая по команде из бота, предназначенная для добавления валют в бд
@dp.message_handler(commands=['manage_currency'])
async def manage_comand(message: types.Message):
    if str(message.from_user.id) != ADMIN_ID:
        await message.answer("У Вас нет доступа к команде! Вы обычный смертный пользователь.")
        await bot.set_my_commands(user_commands, scope=BotCommandScopeDefault())
    else:
        await message.answer("О, Вы Админ! Введите название конвертируемой валюты:")
        await bot.set_my_commands(admin_commands, scope=BotCommandScopeDefault())

        await Form.save_base.set()


# функция выполняемая по переходу на состояния
@dp.message_handler(state=Form.save_base)
async def save_base(message: types.Message, state: FSMContext):
    await state.update_data(baseCurrency=message.text)  # Сохраняет в память состояния название основной валюты
    await Form.save_converted.set()
    await message.reply("Введите название валюты, в которую будем конвертировать:")


# функция выполняемая по переходу на состояния
@dp.message_handler(state=Form.save_converted)
async def save_converted(message: types.Message, state: FSMContext):
    await state.update_data(code=message.text)  # Сохраняет в память состояния название валюты для конвертации
    await Form.save_converted_rate.set()
    await message.reply("Введите курс:")


# функция выполняемая по переходу на состояния
@dp.message_handler(state=Form.save_converted_rate)
async def save_converted(message: types.Message, state: FSMContext):
    data = await state.get_data()  # записывает в переменню данные из состояния
    code_ = data['code']  # записывает в переменню полученные данные названия конвертируемых валют по ключу
    try:
        rates_ = data['rates']  # записывает в переменню полученные данные курса конвертируемых валют по ключу
    except:
        rates_ = []
    rates_.append({'code': code_, 'rate': float(message.text)})  # записывает в словарь полученные данные
    # конвертируемой валюты по ключам
    await state.update_data(rates=rates_)  # Сохраняет в память состояния название и курс валют для конвертации
    await Form.save.set()
    await message.reply("Добавить еще валюту, в которую может сконвертирована основная валюта. Введите 'Да' или 'Нет'!")


# функция выполняемая по переходу на состояния
@dp.message_handler(state=Form.save)
async def save_converted(message: types.Message, state: FSMContext):
    cur = await state.get_data()  # записывает в переменню данные из состояния
    check = message.text  # записывает в переменню данные из сообщения
    i = "Да"
    if i in check:  # проверяет хотим ли добавить ещё валюты для конвертации, если "Да" то переходим на состояние
        # save_converted
        await message.reply("Введите название валюты, в которую будем конвертировать:")
        await Form.save_converted.set()
    else:  # если в бота пришло любое другое сообщение кроме "Да", то выполняется следующее
        param["baseCurrency"] = str(cur["baseCurrency"])  # записываем в словарь название основной влюты по ключа
        param["rates"] = cur["rates"]  # записываем в словарь данные влют для конвертации по ключа
        requests.post("http://localhost:10690/load", json=param)  # отправляем запрос с данными в микросервис
        await message.reply("Вы завершили настройку валюты!")
        param.clear()  # очищаем словарь
        await state.finish()


# функция выполняемая по команде из бота, предназначенная для конвертации валют
@dp.message_handler(commands=['convert'])
async def convert_comand(message: types.Message):
    await Form.check.set()
    await message.reply("Введите название валюты для конвертации:")


# функция выполняемая по переходу на состояния
@dp.message_handler(state=Form.check)
async def process_check(message: types.Message, state: FSMContext):
    await state.update_data(baseCurrency=message.text)  # Сохраняет в память состояния название основной валюты
    await Form.num.set()
    await message.reply("Введите название валюты, в которую будем конвертировать:")


# функция выполняемая по переходу на состояния
@dp.message_handler(state=Form.num)
async def process_convert(message: types.Message, state: FSMContext):
    await state.update_data(convertedCurrency=message.text)  # Сохраняет в память состояния название валюты для
    # конвертации
    await Form.con.set()
    await message.reply("Введите сумму для конвертации:")


# функция выполняемая по переходу на состояния
@dp.message_handler(state=Form.con)
async def process_convert2(message: types.Message, state: FSMContext):
    num = message.text  # Сохраняет в переменную сумму для конвертации
    cur = await state.get_data()  # записывает в переменню данные из состояния
    param["baseCurrency"] = str(cur["baseCurrency"])  # записываем в словарь название основной влюты по ключа
    param["convertedCurrency"] = str(cur["convertedCurrency"])  # записываем в словарь название влюты для конвертации
    # по ключа
    param["sum"] = str(num)  # записываем в словарь сумму для конвертации
    result = requests.get("http://localhost:10609/convert", params=param)  # отправляем запрос с данными в микросервис
    if result == "<Response [500]>":  # При получении ошибки из микросервиса выполняется следующее
        await message.reply('Произошла ошибка при конвертации валюты :(')
        param.clear()
        await state.finish()
    else:  # При успешном выполнении микросервиса
        res = result.text  # Записываемрезультат выполнения микросервиса в переменную
        res = str(re.sub(r"[^0-9.]", r"", res))  # убираем лишние сиволы
        await message.reply(f'Результат конвертации: {res}')  # Отправляем результат в бота
        param.clear()
        await state.finish()


# точка входа в приложение
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
