from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as iKB

from Keyboards.callback_data import menu
from loader import db


def kb_settings():
    keyboard = InlineKeyboardMarkup()
    for vacancy in db.company_list():
        _, name, table_name, parse_time, active = vacancy
        btn_name = iKB(text=name, callback_data=menu.new(name='link', button=table_name))
        btn_active = iKB(text='✅' if active else '❌', callback_data=menu.new(name='switch', button=name))
        keyboard.row(btn_name, btn_active)
    btn_back = iKB(text='Назад', callback_data=menu.new(name='start', button='start'))
    keyboard.add(btn_back)
    return keyboard
