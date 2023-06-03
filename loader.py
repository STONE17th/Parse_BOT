from os import getenv

from aiogram import Bot, Dispatcher
from Classes import Database


bot = Bot(token=getenv('TOKEN'))
dp = Dispatcher(bot)
db = Database()
