import logging
import os
import psycopg2 as pg
import re
import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from aiogram.types import ReplyKeyboardRemove, \
                          ReplyKeyboardMarkup, KeyboardButton, \
                          BotCommand, BotCommandScopeDefault, BotCommandScopeChat

conn = pg.connect(user     = 'postgres',
                  password = 'postgres',
                  host     = 'localhost',
                  port     = '5432',
                  database = 'RPPLabs')
cursor = conn.cursor()

TOKEN = "6165848339:AAE2sRqeBVZ7ss23Kw9J9zIx-0I7I5mWu5c"
logging.basicConfig(level = logging.INFO)

bot = Bot(token = TOKEN, parse_mode = types.ParseMode.HTML)
dp  = Dispatcher(bot, storage = MemoryStorage())


def get_id(chat_id):
    cursor.execute("""insert into admin(chat_id)
                      values (%s);""", chat_id)
    admin_id = cursor.fetchall()
    conn.commit()

    admin_id = re.sub(r"[^0-9]", r"", str(admin_id))
    admin_list = []
    if admin_id in admin_list:
        return admin_list
    else:
        admin_list.append(admin_id)
        return admin_list


def add_currency(currency):
    cursor.execute("""insert into currency(currency_name, rate) 
                           values (%s, %s);""", currency)
    conn.commit()
    currency.clear()


class Form(StatesGroup):
    name        = State()
    delete_name = State()
    edit_name   = State()
    edit_name1  = State()
    rate        = State()
    check       = State()
    num         = State()
    delete      = State()
    save1       = State()
    save2       = State()
    save3       = State()


currency = []
f_name = []

user_buttons = [
    types.InlineKeyboardButton(text = 'START',                       callback_data = 'start'),
    types.InlineKeyboardButton(text = 'Меню',                        callback_data = 'menu'),
    types.InlineKeyboardButton(text = 'Записать и сохранить валюту', callback_data = 'save_cur'),
    types.InlineKeyboardButton(text = 'Конвертировать',              callback_data = 'convert'),
    types.InlineKeyboardButton(text = 'Список валют',                callback_data = 'show_saves')
]

admin_buttons = [
    types.InlineKeyboardButton(text = 'START',                       callback_data = 'start'),
    types.InlineKeyboardButton(text = 'Меню',                        callback_data = 'menu'),
    types.InlineKeyboardButton(text = 'Записать и сохранить валюту', callback_data = 'save_cur'),
    types.InlineKeyboardButton(text = 'Конвертировать',              callback_data = 'convert'),
    types.InlineKeyboardButton(text = 'Список валют',                callback_data = 'show_saves'),
    types.InlineKeyboardButton(text = 'Редактировать валюту',        callback_data = 'edit_cur'),
    types.InlineKeyboardButton(text = 'Удалить Валюту',              callback_data = 'delete_currency'),
    types.InlineKeyboardButton(text = 'Показать ID',                 callback_data = 'id')
]

# Создание объекта класса InlineKeyboardMarkup с передачей списка кнопок в конструктор для Админа и Пользователя
keyboard = types.InlineKeyboardMarkup(row_width = 8)
keyboard.add(*user_buttons)


# Функции команд
# Обработчик для команды /start
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await bot.send_message(message.chat.id, "Привет! Я бот для конвертации валюты. Для начала, выбери обозначение валюты с помощью действия ниже.")
    await bot.send_message(message.chat.id, "Вы Админ! Выберите действие:", reply_markup=admin_buttons)

    admin_id = get_id()
    admin = str(message.chat.id)
    if admin in admin_id:
        await bot.send_message(message.chat.id, "Вы Админ! Выберите действие:", reply_markup=admin_buttons)
    else:
        await bot.send_message(message.chat.id, "Вы Пользователь:", reply_markup=user_buttons)


# Обработчик для команды /help
@dp.message_handler(commands = ['help'])
async def help_handler(message: types.Message):
    await bot.send_message(message.chat.id, "Я помогу тебе конвертировать из любой валюты в любую валюту и наоборот. Просто нажми => /start и следуй инструкции.")


# Обработчик команды 'Показать ID'
@dp.message_handler(commands=['id'])
async def let_id(message: types.Message):
    await message.answer("Ваш ID:", message.chat.id)


# Обработчик для команды 'Записать и сохранить валюту'
@dp.callback_query_handler(lambda c: c.data == 'save_cur')
async def save_cur(message: types.Message):
    admin_id = get_id()
    admin    = str(message.chat.id)

    if admin in admin_id:
        await bot.send_message(message.chat.id, "Введите название валюты для сохранения в коллекцию: ")
        await Form.name.set()
    else:
        await bot.send_message(message.chat.id, "Нет доступа к команде :(")

@dp.message_handler(state = Form.name)
async def process_name(message: types.Message, state: FSMContext):
    currency.append(message.text)
    await Form.rate.set()
    await bot.send_message(message.chat.id, "Введите курс валюты для записи:")
    await state.finish()


@dp.message_handler(state = Form.rate)
async def process_rate(message: types.Message, state: FSMContext):
    currency.append(message.text)
    add_currency(currency)
    await bot.send_message(message.chat.id, "Валюта сохранена!")
    await state.finish()

@dp.callback_query_handler(state = Form.save2)
async def process_save2(message: types.Message, state: FSMContext):
    name = message.text
    curr = cursor.execute("""select currency_name 
                               from currency 
                              where currency_name = %s""",(name,))
    curr = cursor.fetchone()

    if curr is None:
        currency.append(name)
        await message.answer("Введите курс валюты для записи:")
        await Form.save3.set()
    else:
        await message.answer("Данная валюта уже существует! Попробуйте ввести другую..")
    await state.finish()


@dp.message_handler(state = Form.save3)
async def process_save3(message: types.Message, state: FSMContext):
    rate = message.text
    currency.append(rate)
    add_currency(currency)
    await message.answer("Валюта сохранена!")
    await state.finish()


# Обработчик команды 'Список валют'
@dp.callback_query_handler(lambda c: c.data == 'show_saves')
async def show_saves(callback_query: types.CallbackQuery):
    cursor.execute("""select currency_name, rate from currency""")
    curr = cursor.fetchall()
    await bot.send_message(callback_query.message.chat.id, str(curr)) # Показывает сохранённые валюты
    await bot.answer_callback_query(callback_query.message.message_id)

@dp.message_handler(lambda c: c.data == 'delete_currency')
async def delete_currency(message: types.Message):
    admin_id = get_id()
    admin = str(message.chat.id)
    if admin in admin_id:
        await Form.delete_name.set()
        await bot.send_message(message.chat.id, "Введите название валюты:")
    else:
        await bot.send_message(message.chat.id, "Нет доступа к команде!")

@dp.message_handler(state = Form.delete_name)
async def process_delete_name(message: types.Message, state: FSMContext):
    name = message.text
    cursor.execute("""delete from currency
                            where currency_name = %s""", (name,))
    conn.commit()
    await bot.send_message(message.chat.id, 'Валюта удалена!')
    await state.finish()


# Обработчик для кнопки 'Редактировать валюту'
@dp.message_handler(lambda c: c.data == 'edit_cur')
async def edit_currency(message: types.Message):
    admin_id = get_id()
    admin = str(message.chat.id)
    if admin in admin_id:
        await Form.edit_name.set()
        await bot.send_message(message.chat.id, "Введите название валюты:")
    else:
        await bot.send_message(message.chat.id, "Нет доступа к команде!")

@dp.message_handler(state = Form.edit_name)
async def process_edit_name(message: types.Message, state: FSMContext):
    name = message.text
    f_name.append(name)
    await Form.edit_name1.set()
    await bot.send_message(message.chat.id, 'Введите новый курс к рублю:')
    await state.finish()

@dp.message_handler(state = Form.edit_name1)
async def process_edit_name1(message: types.Message, state: FSMContext):
    rate = message.text
    cursor.execute("""update currency set rate = %s where currency_name = %s""", (rate, f_name[0],))
    conn.commit()
    await bot.send_message(message.chat.id, 'Информация о валюте обновлена!')
    f_name.clear()
    await state.finish()


# Обработчик для кнопки 'Конвертировать валюту'
@dp.message_handler(lambda c: c.data == 'convert')
async def convert_currency(message: types.Message):
    await Form.check.set()
    await bot.send_message(message.chat.id, "Введите название валюты для конвертации:")

@dp.message_handler(state=Form.check)
async def process_check(message: types.Message,
                        state:   FSMContext):
    await state.update_data(check_rate=message.text)
    name = message.text
    cursor.execute("""select rate from currency where lower(currency_name) = %s""", (name,))
    rate = cursor.fetchone()
    if rate:
        rate = float(rate[0])
        await Form.num.set()
        await bot.send_message(message.chat.id, "Введите сумму перевода:")
    else:
        await bot.send_message(message.chat.id, "Такая валюта не найдена!")
    await state.finish()

@dp.message_handler(state = Form.num)
async def process_num(message: types.Message,
                      state:   FSMContext):
    num    = message.text
    data   = await state.get_data()
    rate   = float(data['check_rate'])
    result = rate * float(num)
    await bot.send_message(message.chat.id, f"Результат конвертации: {result}")
    await state.finish()


#точка входа в приложение
if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO)
    executor.start_polling(dp, skip_updates = True)