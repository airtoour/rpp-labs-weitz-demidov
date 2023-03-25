#Настройка Бота
import aiogram
import os

from aiogram import dispatcher, executor, types, bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

API_TOKEN = os.environ

bot = Bot(API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStage())

class States(StatesGroup):
    REGISTER_PROCESS = State()

users = {}

@dp.message.handlers(command=['reg', 'singup', 'register'])
async def register_process(message: types.Messege):
    await States.REGISTER_PROCESS.set()
    await message.answer("Введите Ваше имя: ")

@dp.message.handlers(command=States.REGISTER_PROCESS)
async def register_name_process(message: types.Message, state: FSMContext):
    name = message.text
    users[name] = message.from_user.id
    await state.finish()

if __name__ == '__main__':
    executor.sart_polling(dp, skip_updates=True)
