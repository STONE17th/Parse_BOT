from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as iKB


def kb_link(url: str):
    keyboard = InlineKeyboardMarkup()
    btn_url = iKB(text='Ссылка', url=url)
    keyboard.add(btn_url)
    return keyboard
