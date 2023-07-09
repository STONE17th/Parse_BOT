import json

from aiogram.types import Message, CallbackQuery

from loader import bot, dp, db
from Keyboards import kb_start
from Keyboards.callback_data import menu
from DataBase.sqla import Vacancies
from Parser.app import outside_crutch

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
def install_com(message: Message):
    base_db = outside_crutch()
    for company in base_db.values():
        for vacancy in company:
            # print(i['company'], i['name'], i['url'], i['parse_time'])
            sdb.add((Vacancies(company=vacancy['company'],
                               name=vacancy['name'],
                               url=vacancy['url'],
                               parse_time=vacancy['parse_time'],
                               status=0)))


@dp.message_handler(commands=['my_id'])
async def my_id(message: Message):
    print(message.from_user.id)