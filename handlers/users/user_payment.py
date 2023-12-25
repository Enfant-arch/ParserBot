from dataclasses import Field
import os
import string
from unittest import result
from aiogram import Dispatcher, Bot
from datetime import datetime
from aiogram import types
from aiogram.types import ContentTypes
from aiogram.dispatcher import FSMContext
from aiogram.types import (Message, KeyboardButton, ReplyKeyboardMarkup,  CallbackQuery, InlineKeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup)
from keyboards.default.menu import payment_serviece
from loader import dp, bot
from keyboards.inline.inline_payment import profile_InlineBoard, crypto_payment, after_pay
from states.Payment_state import Payment, PaymentCredit
from aiogram.types import ParseMode
import logging
from aiogram.types import animation
from aiogram.dispatcher.filters import Text
from keyboards.default import check_user_out_func
from middlewares.throttling import rate_limit
from utils.payment.currency_payment import CurrencyPayment
from utils.payment.env import MinPay, PROJECT_NAME, curr
from utils.db_api.psql  import *
from utils.payment import lolzapi
from admin_panel.panel.core import core


currency = "RUB"







"""###Make promocode payment method
@dp.callback_query_handler( lambda x: x.data == 'promoBy')
async def selectPromoPay(msg: Message, state: FSMContext):
    await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message.message_id)
    x = InlineKeyboardButton("Отменить оплату", callback_data="cancel")
    await bot.send_message(text="Введите ваш промокод", chat_id=msg.from_user.id, reply_markup=InlineKeyboardMarkup(row_width=1).add(x))
    await PromoPay.promo.set()

@dp.message_handler(state=PromoPay.promo)
async def get_Promo(msg : types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['promo'] = msg.text
        money = await PromoCode.check_promo(promo=data["promo"], msg=msg)
    if money == None:
        await msg.answer("Такого промокода нет")
        await state.finish()
    else:
        money = money[0] 
        await User_Db.upBalance(msg.from_user.id, value=int(money))
        await msg.answer(f"На ваш счёт зачисленно {money} $")
        await PromoCode.remoove_promo(data["promo"])
        await state.finish()"""





#?Options in Payment time
#*canncel PAY
@dp.callback_query_handler( lambda x: x.data == "cancel",state='*')
async def cancel_handler(msg: types.Message, state: FSMContext):
    await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message.message_id )
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(text='Оплата отмененна', chat_id=msg.from_user.id, reply_markup=profile_InlineBoard)



async def QRCODE(msg, addres, amount, curency):
    await bot.send_photo(msg.chat.id, photo=f"https://chart.googleapis.com/chart?chs=300x300&chld=L|2&cht=qr&chl={curency}:{addres}?amount={amount}%26label={PROJECT_NAME}%26message=payment",
    parse_mode=ParseMode.MARKDOWN_V2, caption=f"\nАдресс: `{addres}`")
    
    

def comment_generation(id=0):
    cmnt=""
    for i in range(7):
            cmnt+=random.choice(string.ascii_letters)
    if id != 0:
        return str(id)+cmnt
    else:
        return cmnt