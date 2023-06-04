from aiogram.utils import executor
from Handlers import dp
from loader import db, load_ini


async def on_start(_):
    print('Bot started')
    db.create_tables_list()
    load_ini()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_start)
