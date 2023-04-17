import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message

TOKEN = "6165848339:AAE2sRqeBVZ7ss23Kw9J9zIx-0I7I5mWu5c"
logging.basicConfig(level = logging.INFO)

bot = Bot(token = TOKEN)
dp = Dispatcher(bot = bot)

# Создание списка кнопок
buttons = [
    types.InlineKeyboardButton(text = 'В Доллар', callback_data = 'rub_to_usd'),
    types.InlineKeyboardButton(text = 'В Рубль', callback_data = 'usd_to_rub')
]

# Создание объекта класса InlineKeyboardMarkup с передачей списка кнопок в конструктор
keyboard = types.InlineKeyboardMarkup(row_width=2)
keyboard.add(*buttons)

# Опредение названия валют и их курсы
RUB = 'RUB'
USD = 'USD'

rub_to_usd = 0.013
usd_to_rub = 75.69

# Определите глобальные переменные для хранения пользовательских входных данных
curr_data = None
curr_amount = None


# Обработчик для команды /start
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    global curr_data
    await message.reply(f"Привет! Я бот, который умеет конвертировать валюты. Для начала, выбери обозначение валюты с помощью действия ниже.")
    await message.reply("Выберите действие:", reply_markup=keyboard)


# Обработчик для команды /help
@dp.message_handler(commands=['help'])
async def help_handler(message: types.Message):
    await message.reply("Я помогу тебе конвертировать из RUB в USD и наоборот. Просто выбери обозначение валюты с помощью кнопок на клавиатуре ниже.")


# Обработчик для обработки нажатия на кнопок
@dp.callback_query_handler(lambda callback_query: True)
async def callback_button_rub(callback_query: types.CallbackQuery):
    global curr_data
    global curr_amount
    # Получение данных о нажатой кнопке
    curr_data = callback_query.data

    # Отправка сообщения пользователю с текстом, соответствующим нажатой кнопке
    if curr_data == 'rub_to_usd':
        await bot.send_message(callback_query.from_user.id, f"Конвертация в доллар.")
        await bot.send_message(callback_query.from_user.id, f"Хорошо, а теперь напиши кол-во денег для конвертации: ")
    elif curr_data == 'usd_to_rub':
        await bot.send_message(callback_query.from_user.id, f"Конвертация в рубль.")
        await bot.send_message(callback_query.from_user.id, f"Хорошо, а теперь напиши кол-во денег для конвертации: ")
    else:
        await bot.send_message(callback_query.from_user.id, f"Кнопка не сработала...")

# Обрабтчик конвертации 
@dp.message_handler(content_types=['text'])
async def handle_text(message: types.Message):
    global curr_data
    global curr_amount

    try:
        curr_amount = float(message.text)
        if curr_data == 'rub_to_usd':
            usd_amount = curr_amount * rub_to_usd
            await bot.send_message(message.from_user.id, f"{curr_amount:.2f} {RUB} = {usd_amount:.2f} {USD}")
        elif curr_data == 'usd_to_rub':
            rub_amount = curr_amount * usd_to_rub
            await bot.send_message(message.from_user.id, f"{curr_amount:.2f} {USD} = {rub_amount:.2f} {RUB}")
        await bot.send_message(message.from_user.id, f"Для повторной конвертации напишите команду /start")
        
        await message.answer("Работа бота завершена!")
        await bot.close()

    except ValueError:
        await bot.send_message(message.from_user.id, "Неправильный формат числа")
        return
    except Exception as e:
        await bot.send_message(message.from_user.id, f"Произошла ошибка: {e}")
        return

    # Сброс переменных для следующего ввода
    curr_data = None
    curr_amount = None

# Запуск бота для дальнейшей работы
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
