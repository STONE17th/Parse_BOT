from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as iKB
from .callback_data import menu


def kb_link(url: str):
    keyboard = InlineKeyboardMarkup()
    if url:
        btn_new = iKB(text='Удалить', callback_data=menu.new(name='del_vac', button=''))
    else:
        btn_new = iKB(text='Восстановить', callback_data=menu.new(name='rev_vac', button=''))
    btn_url = iKB(text='Ссылка', url=url)
    keyboard.add(btn_new)
    keyboard.add(btn_url)
    return keyboard
