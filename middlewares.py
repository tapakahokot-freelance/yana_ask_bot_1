from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from db import User


class UserMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        chat_id = message.chat.id

        if not chat_id:
            return

        data['user'] = User.get_or_create(chat_id)
        if message.from_user.username and data['user'].username != message.from_user.username:
            data['user'].username = message.from_user.username
            data['user'].save()

    async def on_process_callback_query(self, call: types.CallbackQuery, data: dict):
        await self.on_pre_process_message(call.message, data)
