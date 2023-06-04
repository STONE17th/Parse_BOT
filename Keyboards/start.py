from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as iKB
from loader import db
from .callback_data import menu


def kb_start():
    keyboard = InlineKeyboardMarkup()
    btn_refresh = iKB(text='Запустить все!', callback_data=menu.new(name='start', button='start'))
    btn_settings = iKB(text='Выбрать биржи', callback_data=menu.new(name='start', button='start'))
    keyboard.add(btn_refresh)
    keyboard.add(btn_settings)
    return keyboard







def kb_settings():
    company_list = db.company_list()
    keyboard = InlineKeyboardMarkup()
    btn_list = [iKB(text=f'{cmp[1]} | {cmp[3]}', callback_data=menu.new(name='', button='')) for cmp in company_list]
    for btn in btn_list:
        keyboard.add(btn)
    return keyboard