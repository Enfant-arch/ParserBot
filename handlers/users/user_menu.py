# - *- coding: utf- 8 - *-
from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import curency, change_hwid_price
import aiohttp
from aiogram.types import ReplyKeyboardRemove
import aiohttp
from admin_panel.panel.core import core
import asyncio
import re
from aiogram.types import CallbackQuery
from middlewares.throttling import rate_limit
from keyboards.default import check_user_out_func, all_back_to_main_default
from keyboards.inline import *
from keyboards.inline.parsing import parsing_InlineBoard
from keyboards.inline.inline_page import *
from loader import dp, bot
from states.state_users import *
from utils.other_func import clear_firstname, get_dates


# Разбив сообщения на несколько, чтобы не прилетало ограничение от ТГ
def split_messages(get_list, count):
    return [get_list[i:i + count] for i in range(0, len(get_list), count)]


@dp.callback_query_handler(lambda x: x.data == "parser:back", state="*")
@rate_limit(2)
@dp.message_handler(text="🤖 Парсинг", state="*")
async def show_search(message: types.CallbackQuery, state: FSMContext):
    await state.finish()
    try:
        message.data == "parser:back"
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id - 1)
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id)
        await bot.send_photo( chat_id=message.from_user.id,
            photo="https://berikod.ru/storage/images/blog/5084d11bbc53b92cd741629a97603fc1_700x350.png", 
            caption="Найдите нужные вам товары с хорошим кешбеком\n<b>👇 Выберите вариант :</b>", reply_markup=parsing_InlineBoard)
    except:
        await bot.send_sticker(chat_id=message.from_user.id, sticker="CAACAgIAAxkBAAELBoJlhykJ0zhIXzUOHr1GJR-yJpBBiwACTgIAAladvQow_mttgTIDbzME", reply_markup=ReplyKeyboardRemove())
        await bot.send_photo( chat_id=message.from_user.id,
            photo="https://berikod.ru/storage/images/blog/5084d11bbc53b92cd741629a97603fc1_700x350.png", 
            caption="Найдите нужные вам товары с хорошим кешбеком\n<b>👇 Выберите вариант :</b>", reply_markup=parsing_InlineBoard)
        


# Обработка кнопки "Профиль"
@dp.callback_query_handler(lambda x: x.data == "back_profile")
@rate_limit(2)
@dp.message_handler(text="👤 Профиль", state="*")
async def show_profile(message: types.Message, state: FSMContext):
    try:
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id )
    except Exception:
        pass
    await state.finish()
    await bot.send_message(chat_id=message.from_user.id, text=get_user_profile(message.from_user.id), reply_markup=open_profile_inl)


# Обработка кнопки "FAQ"
@dp.message_handler(text="ℹ FAQ", state="*")
@rate_limit(2)
async def show_my_deals(message: types.Message, state: FSMContext):
    await state.finish()
    get_settings = get_settingsx()
    send_msg = get_settings[1]
    core.logger.make_log(send_msg)
    fqboard = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text="Читать", url=send_msg))
    await message.answer("FAQ", disable_web_page_preview=False, reply_markup=fqboard)


