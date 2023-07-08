from os import getenv

from aiogram import Bot, Dispatcher
from Classes import Database

PATH = 'DataBase/files_list.ini'
DB_PATH = 'DataBase/parse_bot_db.db'
LIST_NEW_VACANCIES = 'DataBase/JSON/list_new_vacancies.json'


bot = Bot(token=getenv('TOKEN'))
dp = Dispatcher(bot)
db = Database(bot)
