# - *- coding: utf- 8 - *-
import json
import random
import time

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.default import all_back_to_main_default, check_user_out_func, payment_serviece, crypto_service
from keyboards.inline import *
from loader import dp, bot
from admin_panel.filters import IsMember
from states.state_payment import StorageQiwi
from utils import send_all_admin, clear_firstname, get_dates
from utils.db_api.psql  import update_userx, get_refillx, add_refillx
from data.config import api_zelenka, id_zelenka, login_zelenka
from data.config import crystal_secret, crystal_salt, login_crystal
from utils.payment import lolzapi
from utils.payment.crystal import CrystalPAY, PayoffSubtractFrom, InvoiceType
from states.Payment_state import Payment, PaymentCredit
from aiogram.types import ReplyKeyboardRemove





lolz = lolzapi.LolzteamApi(api_zelenka, id_zelenka)
crystal_pay = CrystalPAY(auth_login=login_crystal, auth_secret=crystal_secret, salt=crystal_salt)




@dp.callback_query_handler(text="user_input")
async def input_amount(call: CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(chat_id=call.from_user.id, text="💰Выберите способ оплаты:", reply_markup=payment_serviece())






@dp.callback_query_handler(text_startswith="way:")
async def input_amount(call: CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    way_pay = call.data[4:]
    if way_pay == "crypto":
        await bot.send_message(chat_id=call.from_user.id, text="Выберите удобную вам валюту...", reply_markup=crypto_service())

    if way_pay == "credit":
        await bot.send_message(chat_id=call.from_user.id, text=f"Укажите сумму пополнения:", reply_markup=ReplyKeyboardRemove())
        await PaymentCredit.money.set()

