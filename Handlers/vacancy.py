from aiogram.types import Message

from loader import dp
from Keyboards import kb_link


@dp.message_handler(commands=['check'])
async def start_com(message: Message):
    vac_list = app.check()
    for vac in vac_list.vacancies:
        text = f'Биржа: {vac_list.company}\nОбновление: {vac_list.parse_time}\n\n'
        await message.answer(text=text + vac.position,
                             reply_markup=kb_link(vac.url))