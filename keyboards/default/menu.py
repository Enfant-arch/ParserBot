# - *- coding: utf- 8 - *-
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from admin_panel.entities.admin import Admin


async def generate_keyboard(user_id) -> InlineKeyboardMarkup:
    if int(user_id) in Admin.admins():
        menu_default = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📰 Информация о боте", callback_data="bot:info")],
            [InlineKeyboardButton(text="⚙ Настройки", callback_data="bot:settings")],
            [InlineKeyboardButton(text="🔆 Общие функции", callback_data="bot:utils")],
        ])
        return menu_default
    else:
        menu_default = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🤖 Парсинг", callback_data="parsing")],
            [InlineKeyboardButton(text="👤 Профиль", callback_data="profile")],
            [InlineKeyboardButton(text="📬 Авторассылка", callback_data="mega-broadcast")],
        ])
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
