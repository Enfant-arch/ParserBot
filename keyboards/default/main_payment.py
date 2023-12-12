# - *- coding: utf- 8 - *-
from aiogram.types import ReplyKeyboardMarkup

from utils.db_api.psql  import get_paymentx


def payment_default():
    payment = get_paymentx()
    payment_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    payment_kb.row("🥝 Изменить QIWI 🖍", "🥝 Проверить QIWI ♻", "🥝 Баланс QIWI 👁")
    if payment[5] == True:
        payment_kb.row("🔴 Выключить пополнения")
    else:
        payment_kb.row("🟢 Включить пополнения")
    payment_kb.row("⬅ На главную")
    return payment_kb

def token_error():
        payment_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        payment_kb.add("Ввести токен 🖍")
        payment_kb.add("Отмена")
