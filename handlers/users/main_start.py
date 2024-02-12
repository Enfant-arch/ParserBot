# - *- coding: utf- 8 - *-

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from admin_panel.panel.core import core
from filters import IsWork, IsUser
from filters.all_filters import IsParse
from keyboards.default import check_user_out_func
from loader import dp, bot
from states import StorageUsers
from utils.db_api.psql  import *
from middlewares.throttling import rate_limit
from utils.other_func import clear_firstname, get_dates

prohibit_buy = ["xbuy_item", "not_buy_items", "buy_this_item", "buy_open_position", "back_buy_item_position",
                "buy_position_prevp", "buy_position_nextp", "buy_category_prevp", "buy_category_nextp",
                "back_buy_item_to_category", "buy_open_category"]


# Проверка на нахождение бота на технических работах
@dp.message_handler(IsWork(), state="*")
@dp.callback_query_handler(IsWork(), state="*")
async def send_work_message(message: types.Message, state: FSMContext):
    x = IsWork()
    if "id" in message:
        await message.answer("🔴 Бот находится на технических работах.")
    else:
        await message.answer("<b>🔴 Бот находится на технических работах.</b>")


@dp.message_handler(text="⬅ На главную", state="*")
@rate_limit(2)
@dp.callback_query_handler(lambda x: x.data == "Home")
@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    first_name = clear_firstname(message.from_user.first_name)
    get_user_id = get_userx(user_id=message.from_user.id)
    if get_user_id is None:
        await message.answer(text="Добро пожаловать в парсер бот по Мегамаркету", reply_markup=await check_user_out_func(message.from_user.id))
        if message.from_user.username is not None:
            get_user_login = get_userx(user_login=message.from_user.username)
            if get_user_login is None:
                add_userx(message.from_user.id, message.from_user.username.lower(), first_name, 0, 0, get_dates())
            else:
                delete_userx(user_login=message.from_user.username)
                add_userx(message.from_user.id, message.from_user.username.lower(), first_name, 0, 0, get_dates())
        else:
            add_userx(message.from_user.id, message.from_user.username, first_name, 0, 0, get_dates())
    else:
        if first_name != get_user_id[2]:
            update_userx(get_user_id[0], user_login=first_name)
        if message.from_user.username is not None:
            if message.from_user.username.lower() != get_user_id[1]:
                update_userx(get_user_id[1], user_login=message.from_user.username.lower())
        try:
            await bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id)    
        except:pass
        await bot.send_message(text="Бот работает стабильно", chat_id=message.from_user.id, reply_markup=await check_user_out_func(message.from_user.id))


@dp.message_handler(IsUser(), state="*")
@dp.callback_query_handler(IsUser(), state="*")
async def send_user_message(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id,
                           "<b>❗ Ваш профиль не был найден.</b>\n"
                           "▶ Введите /start")


@dp.message_handler(IsParse(), text="🤖 Парсинг", state="*")
@dp.message_handler(IsParse(), state=StorageUsers.here_input_count_buy_item)
@dp.callback_query_handler(IsParse(), text_startswith=prohibit_buy, state="*")
async def send_user_message(message, state: FSMContext):
    if "id" in message:
        await message.answer("🔴 Покупки в боте временно отключены", True)
    else:
        await message.answer("<b>🔴 Покупки в боте временно отключены</b>")
