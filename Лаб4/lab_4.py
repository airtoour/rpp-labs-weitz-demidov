import os
import logging

from aiogram import Bot, types, executor, Dispatcher

TOKEN = "6165848339:AAE2sRqeBVZ7ss23Kw9J9zIx-0I7I5mWu5c"
logging.basicConfig(level = logging.INFO)

bot = Bot(token = TOKEN)
dp = Dispatcher(bot = bot)

# Опредение названия валют и их курсы
RUB = 'RUB'
USD = 'USD'

rub_to_usd = 0.013
usd_to_rub = 75.69

# Определите глобальные переменные для хранения пользовательских входных данных
curr_name = None
curr_amount = None


# Обработчик для команды /start
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет! Я бот, который умеет конвертировать валюты. Для начала, напиши обозначение валюты, например, 'USD' или 'RUB'. (Пока только имеено такие названия :/)")


# Обработчик для команды /help
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Я помогу тебе конвертировать из RUB в USD и наоборот. Просто напиши обозначение валюты, например, 'USD'.")


# Обработчик вводов пользователя
@dp.message_handler()
async def handle_user_input(message: types.Message):
    global curr_name, curr_amount

    if curr_name is None:
        # Пользователь вводит название валюты
        curr_name = message.text.upper()  # Преобразовать в верхний регистр для недопущения ошибок ввода

        # Проверка на действительность ввода валюты
        if curr_name not in [RUB, USD]:
            await message.reply(f"Неправильное обозначение валюты: {curr_name}")
            curr_name = None  # Сброс названия валюты для следующего ввода
        else:
            await message.reply(f"Хорошо, а теперь напиши кол-во {curr_name} для конвертации")
    else:
        # Пользователь вводит сумму в валюте
        try:
            curr_amount = float(message.text)
            if curr_name == RUB:
                # Конвертация рубля в доллар
                usd_amount = curr_amount * rub_to_usd
                await message.reply(f"{curr_amount:.2f} {RUB} = {usd_amount:.2f} {USD}")
                await message.reply(f"Для повторной конвертации напишите новое название валюты или команду /start")
            else:
                # Конвертация доллара в рубль
                rub_amount = curr_amount * usd_to_rub
                await message.reply(f"{curr_amount:.2f} {USD} = {rub_amount:.2f} {RUB}")
                await message.reply(f"Для повторной конвертации напишите новое название валюты или команду /start")
        except ValueError:
            await message.reply("Неправильный формат числа")
        except Exception as e:
            await message.reply(f"Произошла ошибка: {e}")

        # Сброс переменных для следующего ввода
        curr_name = None
        curr_amount = None

# Запуск бота для дальнейшей работы
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
