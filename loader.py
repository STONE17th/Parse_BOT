from os import getenv

from aiogram import Bot, Dispatcher
from Classes import Database
import DataBase

PATH = 'DataBase/files_list.ini'
ALL_FILES = []

bot = Bot(token=getenv('TOKEN'))
dp = Dispatcher(bot)
db = Database()

def load_ini():
    global ALL_FILES
    with open(PATH, 'r', encoding='UTF-8') as file:
        data = file.readlines()
    for entry in data:
        ALL_FILES.append(entry.strip())
