from aiogram.types import Message

from DataBase import install_db
from loader import dp, db, ALL_FILES, load_ini
from Keyboards import kb_start


@dp.message_handler(commands=['start'])
async def start_com(message: Message):
    company_list = db.company_list()
    text = [f'{cmp[1]}\t\t| {cmp[3]}' for cmp in company_list]
    text = '\n'.join(text)
    await message.answer(text=text, reply_markup=kb_start())


@dp.message_handler(commands=['install'])
async def install_com(message: Message):
    install_db()
    await message.answer('Загрузка завершена')


@dp.message_handler(commands=['list'])
async def install_com(message: Message):
    await message.answer(text=db.company_list())
