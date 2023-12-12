# - *- coding: utf- 8 - *-
from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import curency, change_hwid_price
import aiohttp
import aiohttp
from admin_panel.panel.core import core
import asyncio
import re
from aiogram.types import CallbackQuery
from middlewares.throttling import rate_limit
from keyboards.default import check_user_out_func, all_back_to_main_default
from keyboards.inline import *
from keyboards.inline.parsing import select_parsing_Inline
from keyboards.inline.inline_page import *
from loader import dp, bot
from states.parsing_state import *
from utils.other_func import clear_firstname, get_dates


# Разбив сообщения на несколько, чтобы не прилетало ограничение от ТГ
def split_messages(get_list, count):
    return [get_list[i:i + count] for i in range(0, len(get_list), count)]


        


# Обработка кнопки "Парсинга"
@dp.callback_query_handler(text_startswith = "by")
@rate_limit(2)
async def show_profile(message: types.CallbackQuery, state: FSMContext):
    method  = message.data[3:]
    async with state.proxy() as data:
        data["method"] = method
    match method:
        case "query":
            await bot.edit_message_caption(message_id=message.message.message_id, chat_id=message.from_user.id,
            caption="🎫 Укажите названия товара для поиска", reply_markup=select_parsing_Inline)
        case "category":
            await bot.edit_message_caption(message_id=message.message.message_id, chat_id=message.from_user.id,
            caption="🎫Выберите категорию для поиска", reply_markup=select_parsing_Inline) 
        
    await Parser.input.set()

@dp.message_handler(state=Parser.input)
@rate_limit(2)
async def show_my_deals(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["input"] = message.text
        if data["method"] == "query":
            pass
