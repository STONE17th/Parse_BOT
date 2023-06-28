import asyncio
from aiogram import Bot, Dispatcher
from datetime import datetime
from aiogram.types import Message
from aiogram.utils import executor

bot = Bot(token='5823827805:AAEmTLXixs7EKuK9wI_boGUFWE10PZXQbdw')
dp = Dispatcher(bot)


async def on_start(_):
    print('Бот запущен')

@dp.message_handler(commands=['now'])
async def uname(message: Message = ''):
    print(message.from_user.id)
    print(datetime.now())


async def update_price(message: Message = ''):
    print(datetime.now())
def repeat(coro, loop):
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(DELAY, repeat, coro, loop)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.call_later(DELAY, repeat, update_price, loop)
    executor.start_polling(dp, loop=loop, skip_updates=True, on_startup=on_start)