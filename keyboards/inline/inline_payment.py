from aiogram.types import InlineKeyboardMarkup, InlineQuery
from aiogram.types import InlineKeyboardButton


#* Products 
your_offers = InlineKeyboardButton("🎁Мои покупки", callback_data='my_buy')
referal_program = InlineKeyboardButton("", callback_data="my_licence")
promo_method = InlineKeyboardButton("🌩 Мои Лицензии", callback_data="promoBy")
toHome = InlineKeyboardButton("⬅ На главную", callback_data="Home")
UpBalance = InlineKeyboardButton("💸Пополнить баланс", callback_data='upBalance')
profile_InlineBoard = InlineKeyboardMarkup(row_width=1).add(your_offers, UpBalance, promo_method, toHome)


#* PAYMENTS METHODS ********************#
btc = InlineKeyboardButton("₿ Bitcoin (BTC)", callback_data="BTC")
ltc = InlineKeyboardButton("Ł Litecoin (LTC)", callback_data="LTC")
usdt = InlineKeyboardButton("₮ USDT (TRC20)", callback_data="USDT")
cancel = InlineKeyboardButton("Отменить оплату", callback_data="cancel")
crypto_payment = InlineKeyboardMarkup(row_width=1).add(btc, usdt, ltc,  cancel)
#! after sending adres to pay
payed = InlineKeyboardButton("Оплатил", callback_data="Payed")
after_pay = InlineKeyboardMarkup(row_width=1).add(payed, cancel)




yes = InlineKeyboardButton(text="Да", callback_data="yes")
no = InlineKeyboardButton(text="Нет", callback_data="no")
accept_variants = InlineKeyboardMarkup(row_width=1).add(yes, no)