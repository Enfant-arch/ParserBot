from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from utils import get_settingsx
from utils.db_api.psql  import get_userx
import logging
from admin_panel.entities.admin import Admin

# Проверка на написания сообщения в ЛС бота
class IsPrivate(BoundFilter):
    async def check(self, message: types.Message):
        return message.chat.type == types.ChatType.PRIVATE


# Проверка на возможность покупки товара
class IsBuy(BoundFilter):
    async def check(self, message: types.Message):
        get_settings = get_settingsx()
        if get_settings[3] == True or int(message.from_user.id) in Admin.admins():
            return False
        else:
            return True


# Проверка на технические работы
class IsWork(BoundFilter):
    async def check(self, message: types.Message):
        get_settings = get_settingsx()
        if get_settings[2] == True or int(message.from_user.id) in Admin.admins():
            return False
        else:
            return True


# Проверка на технические работы
class IsUser(BoundFilter):
    async def check(self, message: types.Message):
        get_profile = get_userx(user_id=message.from_user.id)
        if get_profile is not None:
            return False
        else:
            return True
