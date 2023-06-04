from aiogram.types import Message, CallbackQuery

from loader import bot, dp, db
from Keyboards import kb_settings
from Keyboards.callback_data import menu


@dp.callback_query_handler(menu.filter(name='settings'))
async def com_settings(call: CallbackQuery):
    caption = []
    for vacancy in db.company_list():
        _, name, _, parse_time, active = vacancy
        caption.append(f'{name} | {parse_time} | {"Включено"if active else "Выключено"}')
    caption = 'Настройки\n' + '\n'.join(caption)
    await bot.edit_message_text(text=caption, chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                reply_markup=kb_settings())

@dp.callback_query_handler(menu.filter(name='switch'))
async def com_settings(call: CallbackQuery):
    name = call.data.split(':')[-1]
    db.switch_active(name)
    caption = []
    for vacancy in db.company_list():
        _, name, _, parse_time, active = vacancy
        caption.append(f'{name} | {parse_time} | {"Включено"if active else "Выключено"}')
    caption = 'Настройки\n' + '\n'.join(caption)
    await bot.edit_message_text(text=caption, chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                reply_markup=kb_settings())