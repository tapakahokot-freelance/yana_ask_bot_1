from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from settings import settings


class IsAdminFilter(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return str(message.chat.id) in settings.admins
