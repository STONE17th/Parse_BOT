import json

import asyncio
from datetime import datetime
from aiogram.utils import executor
from Handlers import dp
from loader import db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DELAY = 10

db = create_engine('sqlite:///DataBase/vac_db.db')
session = sessionmaker(bind=db)
sdb = session()


async def on_start(_):
    print('Bot starting...')
    print('Checking DataBase... ', end='')
    try:
        db.create_tables_list()
        for path in get_list_of_companies():
            # with open(path, '', encoding='UTF-8') as file:
            #     data = json.load(file)
            db.create_table()
        print('OK!')
    except:
        print('FAILURE!')

    print('Bot is started!')


def repeat(coro, loop):
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(DELAY, repeat, coro, loop)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_start)

    loop = asyncio.get_event_loop()
    loop.call_later(DELAY, repeat, update_price, loop)
    executor.start_polling(dp, loop=loop, skip_updates=True, on_startup=on_start)
