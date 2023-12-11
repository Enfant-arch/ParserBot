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
from keyboards.inline.parsing import parsing_InlineBoard
from keyboards.inline.inline_page import *
from loader import dp, bot
from states.state_users import *
from utils.other_func import clear_firstname, get_dates


# Разбив сообщения на несколько, чтобы не прилетало ограничение от ТГ
def split_messages(get_list, count):
    return [get_list[i:i + count] for i in range(0, len(get_list), count)]


dp.callback_query_handler(lambda x: x.data == "parser:back", state="*")
@rate_limit(2)
@dp.message_handler(text="🤖 Парсинг", state="*")
async def show_search(message: types.Message, state: FSMContext):
    await state.finish()
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
    if "{username}" in send_msg:
        send_msg = send_msg.replace("{username}", f"<b>{message.from_user.username}</b>")
    if "{user_id}" in send_msg:
        send_msg = send_msg.replace("{user_id}", f"<b>{message.from_user.id}</b>")
    if "{firstname}" in send_msg:
        send_msg = send_msg.replace("{firstname}", f"<b>{clear_firstname(message.from_user.first_name)}</b>")
    fqboard = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text="Читать", url=send_msg))
    await message.answer("FAQ", disable_web_page_preview=False, reply_markup=fqboard)


# Обработка кнопки "Поддержка"
@dp.message_handler(text="🦸 Поддержка", state="*")
@rate_limit(2)
async def show_contact(message: types.Message, state: FSMContext):
    await state.finish()
    get_settings = get_settingsx()
    await message.answer(get_settings[0], disable_web_page_preview=True)


# Обработка колбэка "покупки"
@dp.callback_query_handler(text="my_buy", state="*")
@rate_limit(2)
async def show_referral(call: CallbackQuery, state: FSMContext):
    last_purchases = last_purchasesx(call.from_user.id)
    if len(last_purchases) >= 1:
        await call.message.delete()
        count_split = 0
        save_purchases = []
        for purchases in last_purchases:
            save_purchases.append(f"<b>📃 Чек:</b> <code>#{purchases[4]}</code>\n"
                                  f"▶ {purchases[9]} | {purchases[5]}шт | {purchases[6]} {curency}\n"
                                  f"🕜 {purchases[13]}\n"
                                  f"<code>{purchases[10]}</code>")
        await call.message.answer("<b>🛒 Последние 10 покупок</b>\n"
                                  "➖➖➖➖➖➖➖➖➖➖➖➖➖")
        save_purchases.reverse()
        len_purchases = len(save_purchases)
        if len_purchases > 4:
            count_split = round(len_purchases / 4)
            count_split = len_purchases // count_split
        if count_split > 1:
            get_message = split_messages(save_purchases, count_split)
            for msg in get_message:
                send_message = "\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n".join(msg)
                await call.message.answer(send_message)
        else:
            send_message = "\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n".join(save_purchases)
            await call.message.answer(send_message)

        await call.message.answer(get_user_profile(call.from_user.id), reply_markup=open_profile_inl)
    else:
        await call.answer("❗ У вас отсутствуют покупки")
    

@dp.callback_query_handler(text="change_hwid")
@rate_limit(2)
async def change_hwid_licence(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(chat_id=call.from_user.id, text="Введите номер лицензии:")
    await StorageChangeHWID.recipt.set()

#Search LICENCE
@dp.message_handler(state=StorageChangeHWID.recipt)
@rate_limit(2)
async def take_number_licence(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["receipt"] = message.text
    last_purchases = take_more_licence(receipt=message.text, user_id=message.from_user.id)
    if len(last_purchases) == 0 :
        await state.finish()
        await message.answer(text="❗ Такой лицензии нет ❗ \n", reply_markup=open_profile_inl)
    else:
        last_purchases = last_purchases[0]
        if len(last_purchases) >= 1:
            time_stamp = (float(last_purchases[2]) + datetime.datetime.timestamp(datetime.datetime.strptime(last_purchases[16], '%Y-%m-%d %H:%M:%S'))) - datetime.datetime.timestamp(datetime.datetime.now())
            expire = (datetime.datetime.utcfromtimestamp(time_stamp).strftime('%dд %Hч %Mм'))
            if time_stamp <= 0:
                text  = ("❗ Лицензия закончилась \n")
                await message.answer(text=text, reply_markup=open_profile_inl)
            else:
                if last_purchases[3] == 0:
                    text  = ("❗ Лицензия найдена\n"
                        f'<b>🆔 HWID:</b> <span class="tg-spoiler">{last_purchases[1]}</span>\n'
                        f"<b>🕜 Осталось:</b><code>{expire}</code>\n"
                        f"Укажите новый HWID для смены:\n")
                else:
                    text  = ("❗ Лицензия найдена\n"
                        f'<b>🆔 HWID:</b> <span class="tg-spoiler">{last_purchases[1]}</span>\n'
                        f"<b>🕜 Осталось:</b><code>{expire}</code>\n"
                        f"<b>Стоимость смены: </b> <code>{change_hwid_price} {curency}</code>\n"
                        f"Укажите новый HWID для смены:\n")
                    await message.answer(text=text) 
                async with state.proxy() as data: 
                    data["old_hwid"] = last_purchases[1]
                    data["product"] = last_purchases[11]
                
            await StorageChangeHWID.new_hwid.set()
        
        
        else:
            await message.answer("❗ У вас отсутствуют лицензии")
            await message.answer(get_user_profile(message.from_user.id), reply_markup=open_profile_inl)

@dp.callback_query_handler(text="confirm", state=StorageChangeHWID.confirm)
async def confirmation_change_hwid(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    async with state.proxy() as data:
        old = data["old_hwid"]
        new = data["new_hwid"]
        receipt = data["receipt"]
        price = data["price"] 
        link = get_positionsx("*", position_type=2)
        balance = get_userx(user_id = call.from_user.id)[4]

        if balance < price:
             await bot.send_message(chat_id=call.from_user.id, text=f"Ошибка, у вас недостаточно средств", reply_markup=check_user_out_func(call.from_user.id))

        else:
            if link[0] != None:
                link = link[0][13].replace("___", new, 1)
                link = link.replace("___", old, 1)
                result = await auth_licence(link)
                
                if result is True:
                    update_licencex(receipt=receipt, HWID=new)
                    update_licencex(receipt=receipt, change_times=1)
                    update_userx(user_id=call.from_user.id, balance = balance - price)
                    await bot.send_message(chat_id=call.from_user.id, text=f"Hwid лицензии изменен!", reply_markup=check_user_out_func(call.from_user.id))
                else:
                    await bot.send_message(chat_id=call.from_user.id, text=f"<b>Ошибка изменения лицензии</b>😰\nМы уже исправляем ошибку", reply_markup=check_user_out_func(call.from_user.id))

            else:
                await bot.send_message(chat_id=call.from_user.id, text=f"Ошибка, обратитесь в службу поддержки")
        await state.finish()

@dp.callback_query_handler(text="cancel", state=StorageChangeHWID.confirm)
async def confirmation_change_hwid(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(chat_id=call.from_user.id, text="Доделываю")
    await state.finish()




@dp.message_handler(state=StorageChangeHWID.new_hwid)
async def take_newHWID_licence(message: types.Message, state: FSMContext):
    new_HWID = message.text
    async with state.proxy() as data:
        receipt =  data["receipt"]
        data["new_hwid"] = message.text
    last_purchases = take_more_licence(receipt=receipt, user_id=message.from_user.id)[0]
    if last_purchases[3] != 0:
        get_user = get_userx(user_id=message.from_user.id)
        if int(get_user[4]) > change_hwid_price:
            text  = ("❗Проверьте корректность данных❗\n"
                    f'<b> Старый HWID:</b> <code>{last_purchases[1]}</code>\n'
                    f"<b> Новый HWID</b><code>{new_HWID}</code>\n"
                    f"<b >Цена : {change_hwid_price} {curency}</b>")
            
            async with state.proxy() as data:
                data["price"] = change_hwid_price
               
            
            await message.answer(text, reply_markup=confirmation)
            
        else:
            await message.answer("❗ У вас недостаточно средств. Пополните баланс")

    else:
        text = ("❗Проверьте корректность данных❗\n"
                    f'<b>Старый HWID:</b> <code>{last_purchases[1]}</code>\n'
                    f"<b>Новый HWID</b><code>{new_HWID}</code>\n"
                    f"<b>Цена : 0\nСледующая смена HWID : {change_hwid_price}р</b>")
        async with state.proxy() as data:
            data["price"] = 0
        await message.answer(text, reply_markup=confirmation)
    
    await StorageChangeHWID.confirm.set()



# Обработка колбэка "1покупки"
@dp.callback_query_handler(text="my_licence", state="*")
async def show_referral(call: CallbackQuery, state: FSMContext):
    last_purchases = last_licencex(call.from_user.id)
    if len(last_purchases) >= 1:
        
        await call.message.delete()
        count_split = 0
        save_purchases = []
        
        for purchases in last_purchases:
            unix_day_out = int(int(purchases[17]) + int(purchases[2]))
            #day_out = datetime.datetime.strptime('%Y-%m-%d %H:%M:%S', datetime.datetime.utcfromtimestamp(unix_day_out))
            day_out = (datetime.datetime.utcfromtimestamp(unix_day_out).strftime('%Y-%m-%d %H:%M'))
            lost_time = unix_day_out - datetime.datetime.timestamp(datetime.datetime.now())

            if lost_time < 0:
                expire = "0 дней"
            else:
                expire = (datetime.datetime.utcfromtimestamp(lost_time).strftime('%dд %Hч %Mм'))

            save_purchases.append(f"<b>ℹ Номер Лицензии:</b> <code>{purchases[7]}</code>\n"
                                  f'<b>🪪 HWID:</b> <span class="tg-spoiler">{purchases[1]}</span>\n'
                                  f"<b>📅 Дата окончания:</b><code>{day_out}</code>\n"
                                  f"<b>🕜 Осталось:</b><code>{expire}</code>\n"
                                  f"<b>🌩  Лицензия на :</b> <code>{purchases[13]}</code>\n"
                                  f"<b>💴  Цена :</b> <code> {purchases[10]} {curency}</code>")
        await call.message.answer("<b>⚙️ Ваши лицензии :</b>\n"
                                  "➖➖➖➖➖➖➖➖➖➖➖➖➖")
        save_purchases.reverse()
        len_purchases = len(save_purchases)
        logging.info(len_purchases)
        if len_purchases > 4:
            count_split = round(len_purchases / 4)
            count_split = len_purchases // count_split
        if count_split > 1:
            get_message = split_messages(save_purchases, count_split)
            for msg in get_message:
                send_message = "\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n".join(msg)
                await call.message.answer(send_message)
        else:
            send_message = "\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n".join(save_purchases)
            await call.message.answer(send_message)
        
        await call.message.answer("➖➖➖➖➖➖➖➖➖➖➖➖➖", reply_markup=chages_licence)

        
    else:
        await call.answer("❗ У вас отсутствуют лицензии")
        await call.message.answer(get_user_profile(call.from_user.id), reply_markup=open_profile_inl)


################################################################################################
######################################### ПОКУПКА ТОВАРА #######################################
# Открытие категории для покупки
@dp.callback_query_handler(text_startswith="buy_open_category", state="*")
async def open_category_for_buy_item(call: CallbackQuery, state: FSMContext):
    category_id = int(call.data.split(":")[1])
    get_category = get_categoryx("*", category_id=category_id)
    get_positions = get_positionsx("*", category_id=category_id)

    get_kb = buy_item_item_position_ap(0, category_id)
    if len(get_positions) >= 1:
        await call.message.edit_text("<b>👇 Выберите нужный вам товар 📦:</b>",
                                     reply_markup=get_kb)
    else:
        await call.answer(f"❕ Товары в категории {get_category[2]} отсутствуют.")


# Вернутсья к предыдущей категории при покупке
@dp.callback_query_handler(text_startswith="back_buy_item_to_category", state="*")
async def back_category_for_buy_item(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("<b>👇 Выберите нужный вам товар 📦:</b>",
                                 reply_markup=buy_item_open_category_ap(0))


# Следующая страница категорий при покупке
@dp.callback_query_handler(text_startswith="buy_category_nextp", state="*")
async def buy_item_next_page_category(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text("<b>🎁 Выберите нужный вам товар:</b>",
                                 reply_markup=buy_item_next_page_category_ap(remover))


# Предыдущая страница категорий при покупке
@dp.callback_query_handler(text_startswith="buy_category_prevp", state="*")
async def buy_item_prev_page_category(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text("<b>🎁 Выберите нужный вам товар:</b>",
                                 reply_markup=buy_item_previous_page_category_ap(remover))


# Следующая страница позиций при покупке
@dp.callback_query_handler(text_startswith="buy_position_nextp", state="*")
async def buy_item_next_page_position(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])

    await call.message.edit_text("<b>🎁 Выберите нужный вам товар:</b>",
                                 reply_markup=item_buy_next_page_position_ap(remover, category_id))


# Предыдущая страница позиций при покупке
@dp.callback_query_handler(text_startswith="buy_position_prevp", state="*")
async def buy_item_prev_page_position(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])

    await call.message.edit_text("<b>🎁 Выберите нужный вам товар:</b>",
                                 reply_markup=item_buy_previous_page_position_ap(remover, category_id))


# Возвращение к страницам позиций при покупке товара
@dp.callback_query_handler(text_startswith="back_buy_item_position", state="*")
async def buy_item_next_page_position(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])

    await call.message.delete()
    await call.message.answer("<b>🎁 Выберите нужный вам товар:</b>",
                              reply_markup=buy_item_item_position_ap(remover, category_id))


# Открытие позиции для покупки
@dp.callback_query_handler(text_startswith="buy_open_position", state="*")
async def open_category_for_create_position(call: CallbackQuery, state: FSMContext):
    position_id = int(call.data.split(":")[1])
    remover = int(call.data.split(":")[2])
    category_id = int(call.data.split(":")[3])

    

    get_position = get_positionx("*", position_id=position_id)
    get_category = get_categoryx("*", category_id=category_id)
    get_items = get_itemsx("*", position_id=position_id)
    
    if (get_position[3] == 2 ):
        send_msg = f"<b>🎁 Покупка товара:</b>\n" \
               f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
               f"<b>📜 Категория:</b> <code>{get_category[2]}</code>\n" \
               f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n" \
               f"<b>💵 Стоимость:</b>\n\t<code>{get_position[5]}  {curency}/день</code>\n\t<code>{get_position[6]}  {curency}/неделя</code>\n\t<code>{get_position[7]}  {curency}/месяц</code>\n" \
               f"<b>📜 Описание:</b>\n" \
               f"{get_position[8]}\n"
        if len(get_position[9]) >= 5:
            await call.message.delete()
            await call.message.answer_photo(get_position[9],
                                            send_msg,
                                            reply_markup=open_item_func(position_id, remover, category_id))
        else:
            await call.message.edit_text(send_msg,
                                        reply_markup=open_item_func(position_id, remover, category_id))
    else:
        send_msg = f"<b>🎁 Покупка товара:</b>\n" \
                f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                f"<b>📜 Категория:</b> <code>{get_category[2]}</code>\n" \
                f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n" \
                f"<b>💵 Стоимость:</b> <code>{get_position[4]} {curency}</code>\n" \
                f"<b>📦 Количество:</b> <code>{get_items}шт</code>\n" \
                f"<b>📜 Описание:</b>\n" \
                f"{get_position[8]}\n"
        if len(get_position[9]) >= 5:
            await call.message.delete()
            await call.message.answer_photo(get_position[9],
                                            send_msg,
                                            reply_markup=open_item_func(position_id, remover, category_id))
        else:
            await call.message.edit_text(send_msg,
                                        reply_markup=open_item_func(position_id, remover, category_id))


# Выбор кол-ва товаров для покупки
@dp.callback_query_handler(text_startswith="buy_this_item", state="*")
async def open_category_for_create_position(call: CallbackQuery, state: FSMContext):
    position_id = int(call.data.split(":")[1])
    async with state.proxy() as data:
        data["pos_id"] = position_id
    get_items = get_itemsx("*", position_id=position_id)
    get_position = get_positionx("*", position_id=position_id)
    get_user = get_userx(user_id=call.from_user.id)
    if get_position[3] != 2:
        if len(get_items) >= 1:
            if int(get_user[4]) >= int(get_position[3]):
                async with state.proxy() as data:
                    data["here_cache_position_id"] = position_id
                await call.message.delete()
                await StorageUsers.here_input_count_buy_item.set()
                await call.message.answer(f"📦 <b>Введите количество товаров для покупки</b>\n"
                                        f"▶ От <code>1</code> до <code>{len(get_items)}</code>\n"
                                        f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                        f"🏷 Название товара: <code>{get_position[2]}</code>\n"
                                        f"💵 Стоимость товара: <code>{get_position[3]} {curency}</code>\n"
                                        f"💳 Ваш баланс: <code>{get_user[4]} {curency}</code>\n",
                                        reply_markup=all_back_to_main_default)
            else:
                await call.answer("❗ У вас недостаточно средств. Пополните баланс")
        else:
            await call.answer("🎁 Товаров нет в наличии.")
    else : 
        async with state.proxy() as data:
            data["here_cache_position_id"] = position_id
        await call.message.delete()
        await StorageUsers.here_input_timeUsing_product.set()
        buy_btns =  InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text=f"День - {get_position[5]} {curency} ", callback_data="pay_for_day")).add(InlineKeyboardButton(text=f"🔥 Неделя - {get_position[6]} {curency}", callback_data="pay_for_week")).add(InlineKeyboardButton(text=f"❤️‍🔥 Месяц - {get_position[7]} {curency}", callback_data="pay_for_month"))

        await call.message.answer(f"⏳ <b>Выберите вермя подписки </b>\n"
                                f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                        f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n" \
                        f"<b>💵 Стоимость:</b>\n\t<code>{get_position[5]}  {curency}/день</code>\n\t<code>{get_position[6]}  {curency}/неделя</code>\n\t<code>{get_position[7]}  {curency}/месяц</code>\n" \
                        f"<b>📜 Описание:</b>\n", reply_markup=buy_btns)
    

### Выбор времени использования товара
# 1 DAY
@dp.callback_query_handler(lambda x: x.data =="pay_for_day", state=StorageUsers.here_input_timeUsing_product)
async def select_day_subscribe(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        position_id = data["pos_id"]
        data["expire"] = 86400

    get_items = get_itemsx("*", position_id=position_id)
    get_position = get_positionx("*", position_id=position_id)
    get_user = get_userx(user_id=call.from_user.id)
    
    if int(get_user[4]) >= int(get_position[5]):
        async with state.proxy() as data:
            data["here_cache_position_id"] = position_id
            data["to_pay"] =get_position[5]
        await call.message.delete()
        await StorageUsers.here_input_your_HWID.set()
        await call.message.answer(f"📦 <b>Введите ваш HWID</b>\n"
                                        f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                        f"🏷 Название товара: <code>{get_position[2]}</code>\n"
                                        f"💵 Стоимость товара: <code>{get_position[5]} {curency}</code>\n"
                                        f"💳 Ваш баланс: <code>{get_user[4]} {curency}</code>\n",
                                reply_markup=all_back_to_main_default)
    else:
        await call.answer("❗ У вас недостаточно средств. Пополните баланс")
    
# 1 WEEK
@dp.callback_query_handler(lambda x: x.data =="pay_for_week", state=StorageUsers.here_input_timeUsing_product)
async def select_week_subscribe(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        position_id = data["pos_id"]
        data["expire"] = 604800
    get_items = get_itemsx("*", position_id=position_id)
    get_position = get_positionx("*", position_id=position_id)
    get_user = get_userx(user_id=call.from_user.id)
    if int(get_user[4]) >= int(get_position[6]):
        async with state.proxy() as data:
            data["here_cache_position_id"] = position_id
            data["to_pay"] =get_position[6]
        await call.message.delete()
        await StorageUsers.here_input_your_HWID.set()
        await call.message.answer(f"📦 <b>Введите ваш HWID</b>\n"
                                        f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                        f"🏷 Название товара: <code>{get_position[2]}</code>\n"
                                        f"💵 Стоимость товара: <code>{get_position[6]} {curency}</code>\n"
                                        f"💳 Ваш баланс: <code>{get_user[4]} {curency}</code>\n",
                                reply_markup=all_back_to_main_default)
    else:
        await call.answer("❗ У вас недостаточно средств. Пополните баланс")

#1 MONTH
@dp.callback_query_handler(lambda x: x.data =="pay_for_month", state=StorageUsers.here_input_timeUsing_product)
async def select_month_subscribe(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        position_id = data["pos_id"]
        data["expire"] = 2629743
    get_items = get_itemsx("*", position_id=position_id)
    get_position = get_positionx("*", position_id=position_id)
    get_user = get_userx(user_id=call.from_user.id)
    if int(get_user[4]) >= int(get_position[7]):
        async with state.proxy() as data:
            data["here_cache_position_id"] = position_id
            data["to_pay"] =get_position[7]
        await call.message.delete()
        await StorageUsers.here_input_your_HWID.set()
        await call.message.answer(f"📦 <b>Введите ваш HWID</b>\n"
                                        f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                        f"🏷 Название товара: <code>{get_position[2]}</code>\n"
                                        f"💵 Стоимость товара: <code>{get_position[7]} {curency}</code>\n"
                                        f"💳 Ваш баланс: <code>{get_user[4]} {curency}</code>\n",
                                reply_markup=all_back_to_main_default)
    else:
        await call.answer("❗ У вас недостаточно средств. Пополните баланс")
   



@dp.message_handler(state=StorageUsers.here_input_your_HWID)
async def input_hwid(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        position_id = data["here_cache_position_id"]
        to_pay = data["to_pay"]
        time = data["expire"]
    get_items = get_itemsx("*", position_id=position_id)
    get_position = get_positionx("*", position_id=position_id)
    get_user = get_userx(user_id=message.from_user.id)    
    hwid = str(message.text)
    amount_pay = float(to_pay)      
    if float(get_user[4]) >= amount_pay:
        await state.finish()
        
        delete_msg = await message.answer("<b>🎁 Товары подготовлены.</b>",
                                       reply_markup= await check_user_out_func(message.from_user.id))
        await message.answer(text=f"<b>🎁 Вы действительно хотите купить товар(ы)?</b>\n"
                            f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                            f"⚠️ Проверьте корректен ли ваш HWID: <b> {hwid} </b>\n"
                            f"🏷 Название товара: <code>{get_position[2]}</code>\n"
                            f"💵 Стоимость товара: <code>{to_pay} {curency}</code>\n"
                            f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                            f"💰 Сумма к покупке: <code>{amount_pay} {curency}</code>", 
                            reply_markup=confirm_buy_Licence(position_id=position_id, HWID=hwid, time=time,
                                                            message_id=delete_msg.message_id, price=to_pay))

    else:
        await message.answer(f"<b>❌ Недостаточно средств на счете.</b>\n"
                            f"<b>📦 Введите количество товаров для покупки</b>\n"
                            f"▶ От <code>1</code> до <code>{len(get_items)}</code>\n"
                            f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                            f"💳 Ваш баланс: <code>{get_user[4]}</code>\n"
                            f"🏷 Название товара: <code>{get_position[2]}</code>\n"
                            f"💵 Стоимость товара: <code>{get_position[3]} {curency}</code>\n",
                            reply_markup=all_back_to_main_default)
               



# Принятие кол-ва товаров для покупки

@dp.message_handler(state=StorageUsers.here_input_count_buy_item)
async def input_buy_count_item(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        position_id = data["here_cache_position_id"]
    get_items = get_itemsx("*", position_id=position_id)
    get_position = get_positionx("*", position_id=position_id)
    get_user = get_userx(user_id=message.from_user.id)

    if message.text.isdigit():
        get_count = int(message.text)
        amount_pay = int(get_position[3]) * get_count
        if len(get_items) >= 1:
            if 1 <= get_count <= len(get_items):
                if int(get_user[4]) >= amount_pay:
                    await state.finish()
                    delete_msg = await message.answer("<b>🎁 Товары подготовлены.</b>",
                                                     reply_markup= await check_user_out_func(message.from_user.id))

                    await message.answer(f"<b>🎁 Вы действительно хотите купить товар(ы)?</b>\n"
                                         f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                         f"🏷 Название товара: <code>{get_position[2]}</code>\n"
                                         f"💵 Стоимость товара: <code>{get_position[3]} {curency}</code>\n"
                                         f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                         f"▶ Количество товаров: <code>{get_count}шт</code>\n"
                                         f"💰 Сумма к покупке: <code>{amount_pay} {curency}</code>",
                                         reply_markup=confirm_buy_items(position_id, get_count,
                                                                        delete_msg.message_id))
                else:
                    await message.answer(f"<b>❌ Недостаточно средств на счете.</b>\n"
                                         f"<b>📦 Введите количество товаров для покупки</b>\n"
                                         f"▶ От <code>1</code> до <code>{len(get_items)}</code>\n"
                                         f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                         f"💳 Ваш баланс: <code>{get_user[4]}</code>\n"
                                         f"🏷 Название товара: <code>{get_position[2]}</code>\n"
                                         f"💵 Стоимость товара: <code>{get_position[3]} {curency}</code>\n",
                                         reply_markup=all_back_to_main_default)
            else:
                await message.answer(f"<b>❌ Неверное количество товаров.</b>\n"
                                     f"<b>📦 Введите количество товаров для покупки</b>\n"
                                     f"▶ От <code>1</code> до <code>{len(get_items)}</code>\n"
                                     f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                     f"💳 Ваш баланс: <code>{get_user[4]}</code>\n"
                                     f"🏷 Название товара: <code>{get_position[2]}</code>\n"
                                     f"💵 Стоимость товара: <code>{get_position[3]} {curency}</code>\n",
                                     reply_markup=all_back_to_main_default)
        else:
            await state.finish()
            await message.answer("<b>🎁 Товар который вы хотели купить, закончился</b>",
                                reply_markup= await check_user_out_func(message.from_user.id))
    else:
        await message.answer(f"<b>❌ Данные были введены неверно.</b>\n"
                             f"<b>📦 Введите количество товаров для покупки</b>\n"
                             f"▶ От <code>1</code> до <code>{len(get_items)}</code>\n"
                             f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                             f"💳 Ваш баланс: <code>{get_user[4]}</code>\n"
                             f"🏷 Название товара: <code>{get_position[2]}</code>\n"
                             f"💵 Стоимость товара: <code>{get_position[3]} {curency}</code>\n",
                             reply_markup=all_back_to_main_default)


# Отмена покупки товара
@dp.callback_query_handler(text_startswith="not_buy_items", state="*")
async def not_buy_this_item(call: CallbackQuery, state: FSMContext):
    message_id = call.data.split(":")[1]
    await call.message.delete()
    await bot.delete_message(call.message.chat.id, message_id)
    await call.message.answer("<b>☑ Вы отменили покупку товаров.</b>",
                              reply_markup=check_user_out_func(call.from_user.id))


# Согласие на покупку товара
@dp.callback_query_handler(text_startswith="xbuy_item:", state="*")
async def yes_buy_this_item(call: CallbackQuery, state: FSMContext):
    get_settings = get_settingsx()
    delete_msg = await call.message.answer("<b>🔄 Ждите, товары подготавливаются</b>")
    position_id = int(call.data.split(":")[1])
    get_count = int(call.data.split(":")[2])
    message_id = int(call.data.split(":")[3])

    await bot.delete_message(call.message.chat.id, message_id)
    await call.message.delete()

    get_items = get_itemsx("*", position_id=position_id)
    get_position = get_positionx("*", position_id=position_id)
    get_user = get_userx(user_id=call.from_user.id)
    amount_pay = int(get_position[3]) * get_count

    if 1 <= int(get_count) <= len(get_items):
        if int(get_user[4]) >= amount_pay:
            save_items, send_count, split_len = buy_itemx(get_items, get_count)

            if split_len <= 50:
                split_len = 70
            elif split_len <= 100:
                split_len = 50
            elif split_len <= 150:
                split_len = 30
            elif split_len <= 200:
                split_len = 10
            else:
                split_len = 3

            if get_count != send_count:
                amount_pay = int(get_position[3]) * send_count
                get_count = send_count

            random_number = [random.randint(100000000, 999999999)]
            passwd = list("ABCDEFGHIGKLMNOPQRSTUVYXWZ")
            random.shuffle(passwd)
            random_char = "".join([random.choice(passwd) for x in range(1)])
            receipt = random_char + str(random_number[0])
            buy_time = get_dates()

            await bot.delete_message(call.from_user.id, delete_msg.message_id)

            if len(save_items) <= split_len:
                send_message = "\n".join(save_items)
                await call.message.answer(f"<b>🎁 Ваши товары:</b>\n"
                                          f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                          f"{send_message}")
            else:
                await call.message.answer(f"<b>🎁 Ваши товары:</b>\n"
                                          f"➖➖➖➖➖➖➖➖➖➖➖➖➖")

                save_split_items = split_messages(save_items, split_len)
                for item in save_split_items:
                    send_message = "\n".join(item)
                    await call.message.answer(send_message)
            save_items = "\n".join(save_items)

            add_purchasex(call.from_user.id, call.from_user.username, call.from_user.first_name,
                          receipt, get_count, amount_pay, get_position[3], get_position[1], get_position[2],
                          save_items, get_user[4], int(get_user[4]) - amount_pay, buy_time, int(time.time()))
            update_userx(call.from_user.id, balance=get_user[4] - amount_pay)
            await call.message.answer(f"<b>🎁 Вы успешно купили товар(ы) ✅</b>\n"
                                      f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                      f"📃 Чек: <code>#{receipt}</code>\n"
                                      f"🏷 Название товара: <code>{get_position[2]}</code>\n"
                                      f"📦 Куплено товаров: <code>{get_count}</code>\n"
                                      f"💵 Сумма покупки: <code>{amount_pay} {curency}</code>\n"
                                      f"👤 Покупатель: <a href='tg://user?id={get_user[1]}'>{get_user[3]}</a> <code>({get_user[1]})</code>\n"
                                      f"🕜 Дата покупки: <code>{buy_time}</code>",
                                      reply_markup=check_user_out_func(call.from_user.id))
        else:
            await call.message.answer("<b>❗ На вашем счёте недостаточно средств</b>")
    else:
        await state.finish()
        await call.message.answer("<b>🎁 Товар который вы хотели купить закончился или изменился.</b>",
                                  check_user_out_func(call.from_user.id))
    

# Отмена покупки товара
@dp.callback_query_handler(text_startswith="not_buy_licence", state="*")
async def not_buy_this_item(call: CallbackQuery, state: FSMContext):
    message_id = call.data.split(":")[1]
    await call.message.delete()
    await bot.delete_message(call.message.chat.id, message_id)
    await call.message.answer("<b>☑ Вы отменили покупку лицензии</b>",
                              reply_markup=check_user_out_func(call.from_user.id))


# Согласие на покупку товара
@dp.callback_query_handler(text_startswith="x:", state="*")
async def yes_buy_this_item(call: CallbackQuery, state: FSMContext):
    get_settings = get_settingsx()
    delete_msg = await call.message.answer("<b>🔄 Ждите, лицензия выдается...</b>")
    position_id = int(call.data.split(":")[1])
    HWID = str(call.data.split(":")[2])
    message_id = call.data.split(":")[3]
    timer = call.data.split(":")[4]
    amount_pay = call.data.split(":")[5]

    await bot.delete_message(call.message.chat.id, message_id)
    await call.message.delete()
    expire = "0d"
    match int(timer):
        case 86400:
            expire = "1d"
        case 604800:
            expire = "7d"
        case 2629743:
            expire = "30d"

    get_position = get_positionx("*", position_id=position_id)
    addres_for_get = get_positionx("base_path", position_id=position_id)
    get_user = get_userx(user_id=call.from_user.id)
    

    if int(get_user[4]) >= int(amount_pay):
       
        random_number = [random.randint(100000000, 999999999)]
        passwd = list("ABCDEFGHIGKLMNOPQRSTUVYXWZ")
        random.shuffle(passwd)
        random_char = "".join([random.choice(passwd) for x in range(1)])
        receipt = random_char + str(random_number[0])
        buy_time = get_dates()

        await bot.delete_message(call.from_user.id, delete_msg.message_id)
       
        x = addres_for_get[0].replace("___", str(expire), 1)
        x = x.replace("___", HWID, 1) 


       
        

        expire = datetime.datetime.utcfromtimestamp(datetime.datetime.timestamp(datetime.datetime.now()) + float(timer)).strftime('%d-%m-%Y %H:%M:%S')

        licence_added = await auth_licence(x)
        if licence_added is True:
            await call.message.answer(f"<b>🎁 Вы успешно приобрели лицензию ✅</b>\n"
                                    f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                    f"📃 Чек: <code>#{receipt}</code>\n"
                                    f"🏷 Название товара: <code>{get_position[2]}</code>\n"
                                    f"📦 Срок действия : <code>{expire}</code>\n"
                                    f"💵 Сумма покупки: <code>{amount_pay} {curency}</code>\n"
                                    f"👤 Покупатель: <a href='tg://user?id={get_user[1]}'>{get_user[3]}</a> <code>({get_user[1]})</code>\n"
                                    f"🕜 Дата покупки: <code>{buy_time}</code>",
                                    reply_markup=check_user_out_func(call.from_user.id))
            add_purchasex(user_id=call.from_user.id,user_login=call.from_user.username, user_name=call.from_user.first_name,
                        receipt=receipt, item_count=1, item_price=amount_pay, item_price_one_item=amount_pay, item_position_id=get_position[3], item_position_name=get_position[1], item_buy=get_position[2],
                        balance_before=get_user[4], balance_after=float(get_user[4]) - float(amount_pay), buy_date=buy_time, buy_date_unix=int(time.time()))
        
            add_licence(HWID, timer, call.from_user.id, call.from_user.username, call.from_user.first_name,
                        receipt, 1, amount_pay, amount_pay, get_position[3], get_position[1], get_position[2],
                        get_user[4], float(get_user[4]) - float(amount_pay), buy_time, int(time.time()))
        
            update_userx(call.from_user.id, balance=float(get_user[4]) - float(amount_pay))
        else:
            await bot.send_message(chat_id=call.from_user.id, text=f"<b>Ошибка выдачи лицензии</b>😰\nМы уже исправляем ошибку", reply_markup=check_user_out_func(call.from_user.id))
    else:
        await call.message.answer("<b>❗ На вашем счёте недостаточно средств</b>")


async def auth_licence(link):
    async with aiohttp.ClientSession() as session:
        core.logger.make_log(f"Попытка выдачи лицензии : {link}")
        async with session.get(f'{link}') as response:
            body = await response.json()
            if response.status == 200:
                return True
            else:
                await bot.send_message(chat_id=core.main_admin,
                                                  text=f"<b>🟥🟥🟥 Ошибка выдачи лицензии: {link} </code></b>\n\n",
                                                  disable_web_page_preview=True) 
                return False

async def is_url(string):
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    return re.search(pattern, string) is not None