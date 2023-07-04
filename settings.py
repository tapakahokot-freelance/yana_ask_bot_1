from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from loguru import logger

from dataclasses import dataclass
from os import getenv, mkdir, path

load_dotenv()

try:
    mkdir("Logs")
except FileExistsError:
    pass

logger.add('Logs/logs.log', format='{time} {level} {message}',
           level=getenv('LOGGING_LEVEL', 'INFO'), rotation='1 MB', compression='zip')

logger.info('-' * 50)
logger.info('Logging start')


@dataclass
class Settings:
    token: str = None
    admins: list[str] = None
    files: dict[str: str] = None

    bot: Bot = None
    dp: Dispatcher = None

    sentry_dsn: str = getenv('SENTRY_DSN')
    is_testing: bool = getenv('TESTING_MODE') == 'TRUE'

    def __post_init__(self):
        self.token = getenv('TEST_BOT_TOKEN') if self.is_testing else getenv('BOT_TOKEN')
        self.admins = getenv('ADMINS').split(',')

        self.bot = Bot(token=self.token)
        self.dp = Dispatcher(self.bot, storage=MemoryStorage())

        base_dir = path.dirname(path.abspath(__file__))
        files_dir = base_dir + '/files'

        self.files = {
            'day_1_step_2': {
                'id': None,
                'path': files_dir + '/day_1_step_2.jpg'
            },
            'day_1_step_3': {
                'id': None,
                'path': files_dir + '/day_1_step_3.jpg'
            },
            'day_1_step_4': {
                'id': None,
                'path': files_dir + '/day_1_step_4.jpg'
            },
            'day_1_step_5': {
                'id': None,
                'path': files_dir + '/day_1_step_5.jpg'
            },
            'day_1_step_11': {
                'id': None,
                'path': files_dir + '/day_1_step_11.pdf'
            },
            'day_2_step_8': {
                'id': None,
                'path': files_dir + '/day_2_step_8.pdf'
            },
        }


settings = Settings()

import sentry_sdk
sentry_sdk.init(settings.sentry_dsn)
