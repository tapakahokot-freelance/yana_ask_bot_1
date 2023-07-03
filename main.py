from asyncio import create_task

from aiogram import executor

from handlers import *
from middlewares import UserMiddleware
from settings import settings

from loguru import logger
import services


async def on_startup(x):
    logger.info('Bot started')
    create_task(services.run_schedule())


async def on_shutdown(x):
    logger.info('Bot finished')


def setup_middlewares():
    settings.dp.middleware.setup(UserMiddleware())


def start_polling():
    setup_middlewares()
    executor.start_polling(settings.dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
    logger.info('Script finished')


if __name__ == '__main__':
    start_polling()
