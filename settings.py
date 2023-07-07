import pathlib

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.files import JSONStorage
from dotenv import load_dotenv
from loguru import logger

from dataclasses import dataclass
from os import getenv, mkdir, path

load_dotenv()

base_dir = path.dirname(path.abspath(__file__))
files_dir = base_dir + '/files'

try:
    mkdir(base_dir + "/logs")
except FileExistsError:
    pass

logger.add(base_dir + '/logs/logs.log', format='{time} {level} {message}',
           level=getenv('LOGGING_LEVEL', 'INFO'), rotation='1 MB', compression='zip')

logger.info('-' * 50)
logger.info('Logging start')

logger.info(f'{base_dir=}')


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
        self.dp = Dispatcher(self.bot, storage=JSONStorage(pathlib.Path(base_dir + '/storage.json')))

        logger.info(f'storage path: {pathlib.Path(base_dir + "/storage.json")}')

        self.files = {
            'day_1_step_2': {
                'id': None,
                'filename': None,
                'path': files_dir + '/day_1_step_2.jpg'
            },
            'day_1_step_3': {
                'id': None,
                'filename': None,
                'path': files_dir + '/day_1_step_3.jpg'
            },
            'day_1_step_4': {
                'id': None,
                'filename': None,
                'path': files_dir + '/day_1_step_4.jpg'
            },
            'day_1_step_5': {
                'id': None,
                'filename': None,
                'path': files_dir + '/day_1_step_5.jpg'
            },
            'day_1_step_11': {
                'id': None,
                'filename': '8 шагов к поступлению за границу.pdf',
                'path': files_dir + '/day_1_step_11.pdf'
            },
            'day_2_step_8': {
                'id': None,
                'filename': 'Сильный личный бренд.pdf',
                'path': files_dir + '/day_2_step_8.pdf'
            },
            'day_3_step_6_1': {
                'id': None,
                'filename': 'Твои шансы.pdf',
                'path': files_dir + '/day_3_step_6_1.pdf'
            },
            'day_3_step_6_2': {
                'id': None,
                'filename': 'Топ 100 университетов.pdf',
                'path': files_dir + '/day_3_step_6_2.pdf'
            },
            'users_info': {
                'id': None,
                'filename': 'Информация о пользователях.xlsx',
                'path': files_dir + '/users_info.xlsx'
            },
        }


settings = Settings()

import sentry_sdk
sentry_sdk.init(settings.sentry_dsn)
