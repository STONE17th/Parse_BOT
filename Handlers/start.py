from aiogram.types import Message

from DataBase import install_db
from loader import dp, db
from Keyboards import kb_start


@dp.message_handler(commands=['start'])
async def start_com(message: Message):
    await message.answer('Бот готов', reply_markup=kb_start())


@dp.message_handler(commands=['install'])
async def install_com(message: Message):
    install_db()
    await message.answer('Загрузка завершена')


@dp.message_handler(commands=['list'])
async def install_com(message: Message):
    await message.answer(text=db.company_list())
