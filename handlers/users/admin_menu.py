# - *- coding: utf- 8 - *-
from aiogram import types
from aiogram.dispatcher import FSMContext

from admin_panel.entities.admin import Admin
from admin_panel.filters import IsAdmin
from keyboards.default import get_settings_func, payment_default, get_functions_func, items_default
from keyboards.inline import choice_way_input_payment_func
from loader import dp, bot
from utils import get_dates
from utils.db_api.psql  import *


# Разбив сообщения на несколько, чтобы не прилетало ограничение от ТГ
def split_messages(get_list, count):
    return [get_list[i:i + count] for i in range(0, len(get_list), count)]


# Обработка кнопки "Платежные системы"
@dp.message_handler(IsAdmin(), text="🔑 Платежные системыssss", state="*")
async def payments_systems(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("🔑 Настройка платежных системы.", reply_markup=payment_default())
    await message.answer("🥝 Выберите способ пополнения 💵\n"
                         "➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                         "🔸 <a href='https://vk.cc/bYjKGM'><b>По форме</b></a> - <code>Готовая форма оплаты QIWI</code>\n"
                         "🔸 <a href='https://vk.cc/bYjKEy'><b>По номеру</b></a> - <code>Перевод средств по номеру телефона</code>\n"
                         "🔸 <a href='https://vk.cc/bYjKJk'><b>По никнейму</b></a> - "
                         "<code>Перевод средств по никнейму (пользователям придётся вручную вводить комментарий)</code>",
                         reply_markup=choice_way_input_payment_func())


# Обработка кнопки "Настройки бота"
@dp.message_handler(IsAdmin(), text="⚙ Настройки", state="*")
async def settings_bot(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("⚙ Основные настройки бота.", reply_markup=get_settings_func())


# Обработка кнопки "Общие функции"
@dp.message_handler(IsAdmin(), text="🔆 Общие функции", state="*")
async def general_functions(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("🔆 Выберите нужную функцию.", reply_markup=get_functions_func(message.from_user.id))


# Обработка кнопки "Общие функции"
@dp.message_handler(IsAdmin(), text="📰 Информация о боте", state="*")
async def general_functions(message: types.Message, state: FSMContext):
    await state.finish()
    about_bot = get_about_bot()
    await message.answer(about_bot)


# Обработка кнопки "Управление товарами"
@dp.message_handler(IsAdmin(), text="🎁 Управление товарами 🖍", state="*")
async def general_functions(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("🎁 Редактирование товаров, разделов и категорий 📜",
                         reply_markup=items_default)


# Получение БД
@dp.message_handler(IsAdmin(), text="/getbd", state="*")
async def general_functions(message: types.Message, state: FSMContext):
    await state.finish()
    for admin in Admin.admins():
        with open("data/botBD.sqlite", "rb") as doc:
            await bot.send_document(admin,
                                    doc,
                                    caption=f"<b>📦 BACKUP</b>\n"
                                            f"<code>🕜 {get_dates()}</code>")


def get_about_bot():
    show_profit_all, show_profit_day, show_refill, show_buy_day, show_money_in_bot, show = 0, 0, 0, 0, 0, 0
    get_settings = get_settingsx()
    all_users = get_all_usersx()
    show_users = get_all_usersxPREMIUM()
    message = "<b>📰 ВСЯ ИНФОРАМЦИЯ О БОТЕ</b>\n" \
              f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
              f"<b>🔶 Пользователи: 🔶</b>\n" \
              f"ℹ️ FAQ : {get_settings[1]}\n"\
              f"👤 Пользователей: <code>{len(all_users)}</code>\n" \
              f"👑👤 PREMIUM Пользователей: <code>{len(show_users)}</code>\n" \
              f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" 
    return message


# Получение списка всех товаров
@dp.message_handler(IsAdmin(), text="/getitems", state="*")
async def get_chat_id(message: types.Message, state: FSMContext):
    await state.finish()
    save_items = []
    count_split = 0
    get_items = get_all_itemsx()
    len_items = len(get_items)
    if len_items >= 1:
        await message.answer("<b>🎁 Все товары</b>\n"
                             "➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                             "<code>📍 айди товара - данные товара</code>\n"
                             "➖➖➖➖➖➖➖➖➖➖➖➖➖\n")
        for item in get_items:
            save_items.append(f"<code>📍 {item[1]} - {item[2]}</code>")
        if len_items >= 20:
            count_split = round(len_items / 20)
            count_split = len_items // count_split
        if count_split > 1:
            get_message = split_messages(save_items, count_split)
            for msg in get_message:
                send_message = "\n".join(msg)
                await message.answer(send_message)
        else:
            send_message = "\n".join(save_items)
            await message.answer(send_message)
    else:
        await message.answer("<b>🎁 Товары отсутствуют</b>")


# Получение списка всех позиций
@dp.message_handler(IsAdmin(), text="/getposition", state="*")
async def get_chat_id(message: types.Message, state: FSMContext):
    await state.finish()
    save_items = []
    count_split = 0
    get_items = get_all_positionsx()
    len_items = len(get_items)
    if len_items >= 1:
        await message.answer("<b>📁 Все позиции</b>\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n")
        for item in get_items:
            save_items.append(f"<code>{item[2]}</code>")
        if len_items >= 35:
            count_split = round(len_items / 35)
            count_split = len_items // count_split
        if count_split > 1:
            get_message = split_messages(save_items, count_split)
            for msg in get_message:
                send_message = "\n".join(msg)
                await message.answer(send_message)
        else:
            send_message = "\n".join(save_items)
            await message.answer(send_message)
    else:
        await message.answer("<b>📁 Позиции отсутствуют</b>")


# Получение подробного списка всех товаров
@dp.message_handler(IsAdmin(), text="/getinfoitems", state="*")
async def get_chat_id(message: types.Message, state: FSMContext):
    await state.finish()
    save_items = []
    count_split = 0
    get_items = get_all_itemsx()
    len_items = len(get_items)
    if len_items >= 1:
        await message.answer("<b>🎁 Все товары и их позиции</b>\n"
                             "➖➖➖➖➖➖➖➖➖➖➖➖➖\n")
        for item in get_items:
            get_position = get_positionx("*", position_id=item[3])
            save_items.append(f"<code>{get_position[2]} - {item[2]}</code>")
        if len_items >= 20:
            count_split = round(len_items / 20)
            count_split = len_items // count_split
        if count_split > 1:
            get_message = split_messages(save_items, count_split)
            for msg in get_message:
                send_message = "\n".join(msg)
                await message.answer(send_message)
        else:
            send_message = "\n".join(save_items)
            await message.answer(send_message)
    else:
        await message.answer("<b>🎁 Товары отсутствуют</b>")
