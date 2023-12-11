from aiogram.dispatcher.middlewares import BaseMiddleware
from admin_panel.entities.user import User
from admin_panel.panel.core import core

class UserUpdater(BaseMiddleware):
    async def on_pre_process_message(self, message, data):
        if message.text:
            if message.text == "/start":
                if User.is_new(message.from_user.id):
                    User.create(message.from_user.id, message.from_user.username)
        if message.from_user:
            if core.update_username:
                User(message.from_user.id,  message.from_user.username)
            if core.update_activity:
                User(message.from_user.id).be_active()