import json

from aiogram.types import Message, CallbackQuery

from loader import bot, dp, db
from Keyboards import kb_start
from Keyboards.callback_data import menu
from DataBase.JSON import files
from Classes import CompanyVacancy


@dp.callback_query_handler(menu.filter(name='start'))
@dp.message_handler(commands=['start'])
async def start_com(message: Message | CallbackQuery):
    company_list = db.company_list()
    caption = [f'{cmp[1]}\t\t| {cmp[3]}' for cmp in company_list]
    caption = '\n'.join(caption)
    if isinstance(message, Message):
        await message.answer(text=caption, reply_markup=kb_start())
    else:
        await bot.edit_message_text(text=caption, chat_id=message.message.chat.id,
                                    message_id=message.message.message_id,
                                    reply_markup=kb_start())


@dp.message_handler(commands=['install'])
async def install_com(message: Message):
    await message.answer('Начинаем экспорт в DB...')
    for n, path in enumerate(files.values(), 1):
        with open(path, 'r', encoding='UTF-8') as file:
            data = json.load(file)
        await db.update(CompanyVacancy(data), message)
        count = f'{n}/{len(files)}\n'
        await message.answer(count + f'База {data[0].get("company")} загружена')
    await message.answer('Загрузка завершена!')