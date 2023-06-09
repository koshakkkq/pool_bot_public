
import logging

from aiogram import executor
from create import dp, bot
from handler_register import register_handlers
from aiogram.types import Message
from mailing.mailing import scheduler

import asyncio

logging.basicConfig(level=logging.ERROR,format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(pathname)s:%(lineno)d] %(message)s',datefmt='%Y-%m-%d:%H:%M:%S', filename='log.txt')



register_handlers(dp)

#register_handlers(dp)
'''async def on_startup(dp):
    asyncio.create_task(proceed.scheduler())'''

async def on_startup(dp):
    me = await bot.get_me()
    logging.error(f'Running {me.username}')
    asyncio.create_task(scheduler())

if __name__ == '__main__':

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


