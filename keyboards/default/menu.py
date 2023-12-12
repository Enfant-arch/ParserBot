# - *- coding: utf- 8 - *-
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from admin_panel.entities.admin import Admin


async def check_user_out_func(user_id):
 
    menu_default = ReplyKeyboardMarkup(resize_keyboard=True)
    menu_default.row("🤖 Парсинг")
    menu_default.row("👤 Профиль", "🦸 Поддержка")
    menu_default.add(KeyboardButton(text="ℹ FAQ")   )
    if int(user_id) in Admin.admins():
        menu_default.row("🎁 Управление товарами 🖍", "📰 Информация о боте")
        menu_default.row("⚙ Настройки", "🔆 Общие функции")
    return menu_default

def payment_serviece():
    payment_services = InlineKeyboardMarkup(resize_keyboard=True)
    payment_services.row(InlineKeyboardButton(text="💲 Криптовалютой", callback_data="way:crypto"))
    payment_services.row(InlineKeyboardButton(text="💳Картой", callback_data="way:credit")) 
    payment_services.row(InlineKeyboardButton("⬅ Отменить оплату", callback_data="back_profile"))
    return payment_services


def crypto_service():
    btc = InlineKeyboardButton("₿ Bitcoin (BTC)", callback_data="cur:btc")
    ltc = InlineKeyboardButton("Ξ Etherium (ETH)", callback_data="cur:eth")
    usdt = InlineKeyboardButton("₮ USDT (TRC20)", callback_data="cur:usd")
    cancel = InlineKeyboardButton("⬅ Отменить оплату", callback_data="back_profile")
    return InlineKeyboardMarkup(row_width=1).add(btc, usdt, ltc,  cancel)

all_back_to_main_default = ReplyKeyboardMarkup(resize_keyboard=True)
all_back_to_main_default.row("⬅ На главную")
