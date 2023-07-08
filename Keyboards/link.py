from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as iKB
from .callback_data import menu


def kb_link(url: str, index: int):
    keyboard = InlineKeyboardMarkup()
    btn_new = iKB(text='Удалить', callback_data=menu.new(name='del_vac', button=index))
    btn_url = iKB(text='Ссылка', url=url)
    keyboard.add(btn_new, btn_url)
    return keyboard
