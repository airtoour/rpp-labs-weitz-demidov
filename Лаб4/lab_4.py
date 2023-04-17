import logging
from aiogram                            import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state   import State, StatesGroup
from aiogram.dispatcher                 import FSMContext
from aiogram.types                      import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, \
                                               InlineKeyboardMarkup, InlineKeyboardButton, Message

TOKEN = "6165848339:AAE2sRqeBVZ7ss23Kw9J9zIx-0I7I5mWu5c"
logging.basicConfig(level = logging.INFO)

bot = Bot(token = TOKEN)
dp = Dispatcher(bot, storage = MemoryStorage())

# Создание списка кнопок
buttons = [
    types.InlineKeyboardButton(text = 'Меню',                        callback_data = 'menu'),
    types.InlineKeyboardButton(text = 'Записать и сохранить валюты', callback_data = 'save_cur'),
    types.InlineKeyboardButton(text = 'Конвертировать',              callback_data = 'convert'),
    types.InlineKeyboardButton(text = 'Список валют',                callback_data = 'show_saves')
]

# Создание объекта класса InlineKeyboardMarkup с передачей списка кнопок в конструктор
keyboard = types.InlineKeyboardMarkup(row_width=2)
keyboard.add(*buttons)

# Опредение названия валют и их курсы
class Form(StatesGroup):
    name  = State()
    rate  = State()
    check = State()
    num   = State()

currs = {}


# Обработчик для команды /start
@dp.message_handler(commands=['start'])
async def start_handler(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, f"Привет! Я бот для конвертации валюты. Для начала, выбери обозначение валюты с помощью действия ниже.")
    await bot.send_message(callback_query.from_user.id, "Выберите действие:", reply_markup = keyboard)


# Обработчик для команды /help
@dp.message_handler(commands=['help'])
async def help_handler(message: types.Message):
    await message.reply("Я помогу тебе конвертировать из любой валюты в любую валюту и наоборот. Просто нажми => /start и следуй инструкции.")


# Обработчик для команды /save_cur
@dp.callback_query_handler(lambda c: c.data == 'save_cur')
async def save_currency_callback(callback_query: types.CallbackQuery):
    await Form.name.set()
    await bot.send_message(callback_query.from_user.id, "Введите название валюты для сохранения в коллекцию: ")
    await bot.answer_callback_query(callback_query.id)


# Обработчик команды /show_saves
@dp.callback_query_handler(lambda c: c.data == 'show_saves')
async def save_currency_callback(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, currs) # Показывает сохранённые валюты
    await bot.answer_callback_query(callback_query.id)


# Обработчик для команды /convert
@dp.callback_query_handler(lambda c: c.data == 'convert')
async def save_currency_callback(callback_query: types.CallbackQuery):
    await Form.check.set() 
    await bot.send_message(callback_query.from_user.id, "Введите название валюты для конвертации:") # => Вводится название валюты


# Обработчик вывода меню кнопок команды /menu
@dp.callback_query_handler(lambda c: c.data == 'menu')
async def menu_currency_callback(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Выберите действие:", reply_markup = keyboard) # По нажатию на кнопку Меню выводятся кнопки меню


# Обработчик для ввода 
@dp.message_handler(state = Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name = message.text)
    await bot.send_message(message.from_user.id, f'Сколько в одном "'+ message.text +'" рублей?')
    await Form.rate.set()


# Обработчик для вывода названия валюты и ее цены
@dp.message_handler(state=Form.rate)
async def process_rate(message: types.Message, state: FSMContext):
    rate          = message.text
    name          = await state.get_data()
    name_currency = name['name']
    currs[name_currency] = rate
    await state.finish()
    await bot.send_message(message.from_user.id, currs)
    await bot.send_message(message.from_user.id, f'Валюта "'+ name_currency +'" сохранена!')


# Обработчик для ввода количества денег
@dp.message_handler(state = Form.check)
async def process_check(message: types.Message, state: FSMContext):
    await state.update_data(check_rate = message.text)
    await message.answer("Введите сумму валюты для перевода в рубли:")
    await Form.num.set()


# Обработчик для подсчёта валюты
@dp.message_handler(state = Form.num)
async def process_convert(message: types.Message, state: FSMContext):
    num           = message.text
    check_rate    = await state.get_data()
    name_currency = check_rate['check_rate']
    result        = int(currs[name_currency]) * int(num)
    await message.reply(result)
    await state.finish()

    await bot.send_message(message.from_user.id, "Работа бота завершена!")
    await bot.close

# Запуск бота для дальнейшей работы
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)