# - *- coding: utf- 8 - *-
from aiogram.types import ReplyKeyboardMarkup
from utils.db_api.psql  import get_settingsx


def get_settings_func():
    get_settings = get_settingsx()
    settings_default = ReplyKeyboardMarkup(resize_keyboard=True)
    if get_settings[3] == True:
        status_parser = "🔴 Выключить приват парсер"
    else:
        status_parser = "🟢 Включить приват парсер"
    if get_settings[2] == True:
        status_work = "🔴 Отправить на тех. работы"
    else:
        status_work = "🟢 Вывести из тех. работ"
    settings_default.row("ℹ Изменить FAQ 🖍", "📕 Изменить контакты 🖍")
    settings_default.row(status_work, status_parser)
    settings_default.row("⬅ На главную")
    return settings_default
