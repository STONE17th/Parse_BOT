import json

import asyncio
from datetime import datetime
from aiogram.utils import executor
from Handlers import dp
from loader import db
from DataBase.JSON import files
from Classes import CompanyVacancy

DELAY = 10


async def on_start(_):
    print('Bot starting...')
    db.create_tables_list()
    for path in files.values():
        with open(path, 'r', encoding='UTF-8') as file:
            data = json.load(file)
        db.create_table(CompanyVacancy(data))
    print('Bot is started!')


def repeat(coro, loop):
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(DELAY, repeat, coro, loop)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_start)

    loop = asyncio.get_event_loop()
    loop.call_later(DELAY, repeat, update_price, loop)
    executor.start_polling(dp, loop=loop, skip_updates=True, on_startup=on_start)
