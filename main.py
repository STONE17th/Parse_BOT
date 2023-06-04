import json

from aiogram.utils import executor
from Handlers import dp
from loader import db
from DataBase.JSON import files
from Classes import CompanyVacancy


async def on_start(_):
    print('Bot starting...')
    db.create_tables_list()
    for path in files.values():
        with open(path, 'r', encoding='UTF-8') as file:
            data = json.load(file)
        db.create_table(CompanyVacancy(data))
    print('Bot is started!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_start)
