from os import getenv

from aiogram import Bot, Dispatcher
from Classes import Database


PATH = 'DataBase/files_list.ini'
ALL_FILES = []

bot = Bot(token=getenv('TOKEN'))
dp = Dispatcher(bot)
db = Database(bot)
