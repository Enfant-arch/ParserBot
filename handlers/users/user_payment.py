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



@dp.message_handler(lambda message: not message.text.isdigit(), state=Payment.money)
async def process_age_invalid(message: types.Message):
    x = InlineKeyboardButton("Отменить оплату", callback_data="cancel")
    return await message.reply("Укажите **число** к оплате", parse_mode=ParseMode.MARKDOWN_V2, reply_markup=InlineKeyboardMarkup(row_width=1).add(x))
    

@dp.message_handler(lambda message: float(message.text)  < float(MinPay), state=Payment.money)
async def process_age_invalid(message: types.Message):
    x = InlineKeyboardButton("Отменить оплату", callback_data="cancel")
    return await message.reply(f"Минимальная возможная сумма оплатой криптовалютой \- `{MinPay}` **{curr}**", parse_mode=ParseMode.MARKDOWN_V2, reply_markup=InlineKeyboardMarkup(row_width=1).add(x))






@dp.callback_query_handler(text_startswith="cur:")
@rate_limit(2)
async def select_pay(msg: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message.message_id)
    valut = msg.data[4:]
    async with state.proxy() as data:
        data["curr"] = valut

    x = InlineKeyboardButton("Отменить оплату", callback_data="cancel")
    await bot.send_message(text=f"Вы выбрали оплату в {valut}", chat_id=msg.from_user.id, reply_markup=ReplyKeyboardRemove())
    await bot.send_message(text=f"Укажите сумму к оплате в {currency}", chat_id=msg.from_user.id, reply_markup=InlineKeyboardMarkup(row_width=1).add(x))
    await Payment.money.set()

@dp.message_handler(state=PaymentCredit.money)
async def get_amount_money(msg : types.Message, state:FSMContext):
    async with state.proxy() as data:
        await msg.reply(text="😔 К сожалению еще не добавлен метод оплаты картой, воспользуйтесь другим средством пополнения.", reply_markup=payment_serviece())
        await state.finish()


@dp.message_handler(state=Payment.money)
async def get_amount_money(msg : types.Message, state:FSMContext):
    async with state.proxy() as data:
        payment = get_payment_crypto(what_select="*", user_id=msg.from_user.id)
        throwNew = 1
        if payment == []:
                await throw_new(msg=msg, state=state)
        elif payment != []:
            if type(payment) == tuple:
                user_curr = payment[4]
                if data["curr"] == user_curr and payment[3] == 0:
                    await throw_old(except_value=payment[5], address=payment[0], msg=msg, state=state)
                else:
                    await throw_new(msg=msg, state=state)
            elif type(payment) == list:
                for i in payment:
                    if i[4] == data['curr'] and i[3] == 0:
                        await throw_old(except_value=i[5], address=i[0], msg=msg, state=state)
                        throwNew = 0
                        break
            if throwNew == 1:
                logging.info(3)
                await throw_new(msg=msg, state=state)


        await state.finish()


@dp.callback_query_handler(text_startswith="cancelCP:")
@rate_limit(2)
async def user_cancel_pay(call: CallbackQuery, state: FSMContext):
    dates = call.data[9:]
    user_id, cur = dates.split("-")
    if str(call.from_user.id) == str(user_id):
        logging.info(f" {str(user_id)} отменил свой платёж")
        update_payment_crypto(user_id=user_id, currency=cur, status=1)
        await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
    
async def throw_old(except_value, address, msg, state):
    async with state.proxy() as data:
        payment = get_payment_crypto(what_select="*", user_id   =msg.from_user.id)
        if type(payment[0]) == tuple: payment = payment[0]
        excpet_time = datetime.datetime.utcfromtimestamp(float(payment[6]) - datetime.datetime.timestamp(datetime.datetime.now())).strftime('%H:%M')
        price = await CurrencyPayment.currency_converter(amount=str(msg.text), from_val=currency, to_val=data["curr"])
        await bot.send_message(text=f"⚠️ У вас уже есть заявка платежа на `{except_value}` **{str(data['curr']).upper()}**\n**⚠️ Вы можете спокойно отправлять средства на адресс `{payment[0]}`\n**{excpet_time}** - время действия адресса)", chat_id=msg.from_user.id, parse_mode=ParseMode.MARKDOWN)
        update_payment_crypto(user_id=msg.from_user.id, currency=str(data['curr']), except_value=msg.text )
        match data["curr"]:
            case "btc":
                link = f"https://blockchair.com/ru/bitcoin/address/{address}"
            case "eth":
                link = f"https://blockchair.com/ru/ethereum/address/{address}"
            case "trx":
                link = f"https://tronscan.org/#/token20/{address}"

        await QRCODE(msg=msg, addres=address, amount=price, curency=data["curr"])
        await bot.send_message(text=f"💰 Для пополнения баланса, отправьте ** {price} {data['curr']}** на этот адрес\n⏳Время на оплату: 30 минут\nВаш баланс будет пополнен после финального подтверждения сети 🔴🔴🔴\n\n[ТРАНЗАКЦИИ ПО АДРЕССУ]({link})", chat_id=msg.from_user.id,
        reply_markup=check_user_out_func(msg.from_user.id), parse_mode=ParseMode.MARKDOWN)



async def throw_new(msg, state):
    async with state.proxy() as data:
        result_generation = await CurrencyPayment.create_wallet(data["curr"])
        address = result_generation["address"]
        amount = msg.text
        price = await CurrencyPayment.currency_converter(amount=amount, from_val=currency, to_val=data["curr"])
        logging.info(f'data  {data["curr"]}')
        match data["curr"]:
            case "btc":
                link = f"https://blockchair.com/ru/bitcoin/address/{address}"
            case "eth":
                link = f"https://blockchair.com/ru/ethereum/address/{address}"
            case "trx":
                link = f"https://tronscan.org/#/token20/{address}"
        logging.info(address)
        add_payment_crypto(user_id=msg.from_user.id, user_login=str(msg.from_user.get_mention()), address=address, currency=data["curr"], expect_value=price)
        await QRCODE(msg=msg, addres=address, amount=price, curency=data["curr"])
        await bot.send_message(text=f"💰 Для пополнения баланса, отправьте `{price}` **{str(data['curr']).upper()}** на этот адресс\n⏳Время на оплату : **30 минут**\nВаш баланс будет пополнен после **финального** подтверждения сети 🔴🔴🔴\n\n[ТРАНЗАКЦИИ ПО АДРЕССУ]({link})", chat_id=msg.from_user.id,
        reply_markup=check_user_out_func(msg.from_user.id), parse_mode=ParseMode.MARKDOWN)
        logging.info("%r create new payment application", msg.from_user.id)





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