import pandas as pd
import logging

from aiogram                            import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state   import State, StatesGroup
from aiogram.dispatcher                 import FSMContext
from aiogram.types.bot_command_scope    import BotCommandScopeChat, BotCommandScopeDefault
from aiogram.types                      import KeyboardButton, ReplyKeyboardMarkup
import psycopg2 as pg

conn = pg.connect(user     = 'postgres',
                  password = 'postgres',
                  host     = 'localhost',
                  port     = '5432',
                  database = 'RPPLabs')
cursor = conn.cursor()

TOKEN = "6165848339:AAE2sRqeBVZ7ss23Kw9J9zIx-0I7I5mWu5c"
logging.basicConfig(level = logging.INFO)

bot = Bot(token      = TOKEN,
          parse_mode = types.ParseMode.HTML)
dp  = Dispatcher(bot, storage = MemoryStorage())

# Вывод записей из таблицы admin
def get_from_admin():
    cursor = conn.cursor()
    cursor.execute("""select *
                        from admin
                       where id = 1""")
    df       = pd.DataFrame(cursor.fetchall())
    admin_list = []
    admin_id = df
    if admin_id in admin_list:
        return (admin_list)
    else:
        admin_list.append(admin_id)
        return (admin_list)

# Вывод имени всех валют
def select_curr():
    cursor = conn.cursor()
    cursor.execute("""select currency_name 
                        from currency""")
    all_currency = cursor.fetchall()
    return (all_currency)

# Добавить запись в таблицу currency
def add_curr(currency_name, rate):
    cursor = conn.cursor()
    cursor.execute("""insert into currency (currency_name, rate)
                      values (%s, %s)""", (currency_name, rate, ))
    conn.commit()

# Обновление данных в таблице currency по имени валюты
def update_function(currency_name,rate):
    cursor = conn.cursor()
    cursor.execute("""update currency
                         set rate = %s
                       where currency_name = %s""", (rate, currency_name))
    conn.commit()

# Удаление записей в таблице currency
def delete_curr(currency_name):
    cursor = conn.cursor()
    cursor.execute("""delete from currency
                            where currency_name = %s""", (currency_name,))
    conn.commit()

# Вывод валют и их курсов
def select_all_curr(currency_name, rate):
    cursor = conn.cursor()
    cursor.execute("""select currency_name,
                             rate
                        from currency""", (currency_name, rate,))
    df = pd.DataFrame(cursor.fetchall(), columns = ['Валюта', 'Курс'])
    return (df)

# Выбор курса из таблицы валют
def select_rate_at_curr(currency_name):
    cursor = conn.cursor()
    cursor.execute("""select rate 
                        from currency
                       where currency_name = %s""", (currency_name,))
    df = pd.DataFrame(cursor.fetchone())
    if df.empty == True:
        ratee = []
    else:
        ratee = df.iloc[0][0]
    return (ratee)

class States(StatesGroup):
    next_convert   = State()
    start_manage   = State()
    check          = State()
    add_state      = State()
    drop_manage    = State()
    update_manage  = State()
    update_process = State()
    start_convert  = State()

ADMIN_ID = get_from_admin()

user_commands = [
    types.BotCommand(command = "/start",          description="Начать"),
    types.BotCommand(command = "/get_currencies", description="Вывод доступных вылют"),
    types.BotCommand(command = "/convert",        description="Конвертация")
]
# Команды для админов
admin_commands = [
    types.BotCommand(command = "/start",           description="Начать"),
    types.BotCommand(command = "/get_currencies",  description="Вывод доступных вылют"),
    types.BotCommand(command = "/convert",         description="Конвертация"),
    types.BotCommand(command = "/manage_currency", description="SuperUser command")
]

async def setup_bot_commands():
    await bot.set_my_commands(user_commands, scope = BotCommandScopeDefault())
    await bot.set_my_commands(admin_commands, scope = BotCommandScopeChat(chat_id = ADMIN_ID))


# Функции команд
# Обработчик для команды /start
# Команда старт
@dp.message_handler(commands=['start'])
async def start_name_process(message: types.Message):
    await message.answer("""Привет! Я бот для конвертации валюты. Для начала, выбери обозначение валюты с помощью действия ниже.
                            Вот какие команды я знаю:
                            /get_currencies - посмотреть курсы валют,
                            /convert - конвертировать валюту в рубль
                            """)

# Конвертация валюты
@dp.message_handler(commands = ['convert'])
async def start_name_process(message: types.Message):
    await States.start_convert.set()
    await message.answer("Введите название валюты:")


@dp.message_handler (state = States.start_convert)
async def read_process(message: types.Message, state: FSMContext):
    currency = message.text
    await state.update_data(currency = currency)
    await message.answer("Введите сумму в указанной валюте:")
    await States.next_convert.set()


@dp.message_handler (state = States.next_convert)
async def convert_process (message: types.Message, state: FSMContext):
    summ         = message.text
    our_currency = await state.get_data()
    rate         = select_rate_at_curr(our_currency['currency'])
    result       = rate * int(summ)
    await message.reply(result)
    await state.finish()


# Все валюты
@dp.message_handler(commands = ['get_currencies'])
async def start_name_process(message: types.Message):
    df = select_all_curr(currency_name, rate)
    await message.answer(df)

# Команда администратора
@dp.message_handler(commands = ['manage_currency'])
async def start_name_process(message: types.Message):
    buttons = [
        #[
            KeyboardButton(text = "Добавить валюту"),
            KeyboardButton(text = "Удалить валюту"),
            KeyboardButton(text = "Изменить курс валюты"),
        #]
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard          = buttons,
        resize_keyboard   = True,
        one_time_keyboard = True
    )

    if str(message.chat.id) != ADMIN_ID:
        await message.reply("У Вас нет доступа к команде! Вы обычный смертный пользователь))")
    else:
        await message.answer("О, Вы Админ!", reply_markup = keyboard)
        await States.start_manage.set()


# Удаление валюты
@dp.message_handler(lambda message: message.text == 'Удалить валюту',
                    state = States.start_manage)
async def delete_process (message: types.Message, state: FSMContext):
    await message.answer("Введите название валюты:")
    await States.drop_manage.set()

@dp.message_handler (state = States.drop_manage)
async def delete_process (message: types.Message, state: FSMContext):
    currency = message.text
    await state.update_data(currency = str(currency))
    delete_curr(currency)
    await message.answer("Валюта удалена!")
    await state.finish()


# Изменение курса валюты
@dp.message_handler(lambda message: message.text == 'Изменить курс валюты',
                    state = States.start_manage)
async def update_currency_process (message: types.Message, state: FSMContext):
    await message.answer("Введите название валюты:")
    await States.update_manage.set()

@dp.message_handler (state = States.update_manage)
async def update_process (message: types.Message, state: FSMContext):
    currency = message.text
    await state.update_data(currency=currency)
    await message.answer("Введите курс валюты к рублю:")
    await States.update_process.set()

@dp.message_handler (state = States.update_process)
async def update_process (message: types.Message, state: FSMContext):
    rate = message.text
    await state.update_data(rate=rate)
    currency = await state.get_data()
    update_function(currency['currency'], rate)
    await message.answer("Валюта изменена!")
    await state.finish()


# Добавление валюты
@dp.message_handler(lambda message: message.text == 'Добавить валюту',
                    state = States.start_manage)
async def add_currency_process (message: types.Message, state: FSMContext):
    await message.answer("Введите название валюты:")
    await States.check.set()

@dp.message_handler (state=States.check)
async def check_process (message: types.Message, state: FSMContext):
    currency = message.text
    await state.update_data(currency = currency)
    currencies = select_rate_at_curr(currency)
    print(currencies)
    if currencies==[]:
        await message.answer("Введите курс к рублю:")
        await States.add_state.set()
    else:
        await message.reply("Данная валюта уже существует!")

@dp.message_handler (state = States.add_state)
async def add_currency_process(message: types.Message, state: FSMContext):
    rate = message.text

    await state.update_data(rate = rate)

    currency = await state.get_data()
    add_curr(currency['currency'], rate)

    await message.answer("Валюта: " + currency['currency'] + " успешно добавлена!")
    await States.check.set()
    await state.finish()

#точка входа в приложение
if __name__ =='__main__':
    logging.basicConfig(level = logging.INFO)
    executor.start_polling(dp, skip_updates = True)