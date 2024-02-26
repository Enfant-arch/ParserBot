# - *- coding: utf- 8 - *-
import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext
from emoji import emojize
import aiohttp
import aiohttp
from admin_panel.panel.core import core
import asyncio
import re
from aiogram.types import CallbackQuery
from middlewares.throttling import rate_limit
from keyboards.default import generate_keyboard
from keyboards.inline import *
from keyboards.inline.parsing import select_parsing_Inline
from keyboards.inline.inline_page import *
from loader import dp, bot
from states.parsing_state import *
from utils.other_func import make_folder_name, get_dates
from utils.parser import QueryParser
from utils.parser.ResultBuilder import ResultBuilder, BASE_DIR
from utils.parser.test import catalog_list, Main_catalog


awailble_pages = 5



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
            caption="🎫Выберите категорию для поиска", reply_markup=Main_catalog) 
        
    await Parser.input.set()

@dp.message_handler(state=Parser.input)
@rate_limit(2)
async def show_my_deals(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["input"] = message.text
        query = make_folder_name(message.text).lower()
        print(query)
        if data["method"] == "query":
            start_time = datetime.datetime.now()
            PARSER_PROCCES = QueryParser.Parser(query=query)
            await bot.send_message(chat_id=message.from_user.id, text=emojize("Парсер приступил к работе обычно это занимает порядка одной минуты, ожидайте результат"), disable_notification=True)
            await bot.send_sticker(chat_id=message.from_user.id, sticker=r"CAACAgIAAxkBAAEK8Ehldb3DRiGrHhLoTyIgTFrruKQMdgACCEIAAirHmErye5nvt3dE_TME", reply_markup = await generate_keyboard(message.from_user.id))
            await PARSER_PROCCES.queryContextBuilder()
            for i in range(awailble_pages):
                PARSER_PROCCES.page = i
                result = await PARSER_PROCCES.enject_all_data()
                if ((result is TimeoutError)):
                    await bot.edit_message_text(message_id=message.message.message_id, chat_id=message.from_user.id,
                    text="Произошел сбой во время работы парсера\nПовторите попытку", reply_markup=select_parsing_Inline)
                    if (PARSER_PROCCES.page == 0):i -= 1
                    else:continue
                else:         
                    await PARSER_PROCCES.handlerResponce()
                
            rb = ResultBuilder(goods_list=PARSER_PROCCES._products._products, username=make_folder_name(message.from_user.full_name), query=query)
            result_time = datetime.datetime.now() - start_time
            botdata = await bot.get_me()
            await message.answer(f"{rb.message}\nЗаняло время: <code>{result_time}</code>\nВыберите любой тип выгрузки данных\n\n\n@{botdata.username}", reply_markup=await configurate_result_board(message.from_user.full_name, query))
            await state.finish()

@dp.callback_query_handler(text_startswith="catalog_item", state=Parser.input)
@rate_limit(2)
async def show_my_deals(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        departmentCatalog = InlineKeyboardMarkup(row=2)
        back = InlineKeyboardButton(text="◀️Назад", callback_data="catalog_item")
        catalog_id = call.data[13:]
        if (catalog_id.count("_") == 0):
            for item in catalog_list:
                if (item["parentId"] == catalog_id):
                    departmentCatalog.add(InlineKeyboardButton(text=item["title"], callback_data=f"catalog_item:{item['id']}"))
               
            await bot.edit_message_caption(caption=f"Вы перешли в категорию {catalog_id} \n🎫Выберите категорию для поиска",
                                        chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=departmentCatalog)
                
        elif (catalog_id.count("_") > 0 ):
            for item in catalog_list:
                if item["parentId"] == catalog_id:departmentCatalog.add(InlineKeyboardButton(text=item["title"], callback_data=f"catalog_item:{item['id']}"))
            
            core.logger.make_log(len(departmentCatalog.inline_keyboard))
            if (len(departmentCatalog.inline_keyboard) > 2):
                departmentCatalog.add(back)
                await bot.edit_message_caption(caption=f"Вы перешли в категорию \n🎫Выберите категорию для поиска",
                                chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=departmentCatalog)
            
            else:
                query_url, query_title = "", ""
                for item in catalog_list:
                    if item["id"] == catalog_id:
                        query_url = item["collection"]["slug"]
                        query_title = item["title"]
                core.logger.make_log(query_url)
                await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
                query_title = make_folder_name(query_title).lower()
                await bot.send_message(chat_id=call.from_user.id, text=emojize(f"Парсер приступил к работе по запросу : {query_title}\n обычно это занимает порядка одной минуты, ожидайте результат"), disable_notification=True)
                await bot.send_sticker(chat_id=call.from_user.id, sticker=r"CAACAgIAAxkBAAEK8Ehldb3DRiGrHhLoTyIgTFrruKQMdgACCEIAAirHmErye5nvt3dE_TME", reply_markup = await generate_keyboard(call.from_user.id))

                start_time = datetime.datetime.now()

                PARSER_PROCCES = QueryParser.Parser(query=query_url, catalog=True)
                await PARSER_PROCCES.queryContextBuilder()
                for i in range(awailble_pages):
                    PARSER_PROCCES.page = i
                    result = await PARSER_PROCCES.enject_all_data()
                    if ((result is TimeoutError)):
                        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                        text="Произошел сбой во время работы парсера\nПовторите попытку", reply_markup=select_parsing_Inline)
                        if (PARSER_PROCCES.page == 0):i -= 1
                        else : continue
                
                    else:                
                        await PARSER_PROCCES.handlerResponce()
                    
                rb = ResultBuilder(goods_list=PARSER_PROCCES._products._products, username=make_folder_name(call.from_user.full_name), query=query_title[:5])
                result_time = datetime.datetime.now() - start_time
                botdata = await bot.get_me()
                await bot.send_message(text=f"{rb.message}\nЗаняло время: <code>{result_time}</code>\nВыберите любой тип выгрузки данных\n\n\n@{botdata.username}", chat_id=call.from_user.id, reply_markup=await configurate_result_board(call.from_user.full_name, query_title[:5]))
                await state.finish()

@dp.callback_query_handler(text_startswith="resultJson:")
async def get_json_result(call: CallbackQuery):
    userAndQuery = call.data[11:]
    additional_path_ = f"\{str(userAndQuery).split(':')[0]}\{str(userAndQuery).split(':')[1]}"
    await bot.send_document(chat_id=call.from_user.id, document=open(BASE_DIR + additional_path_ + r"\result.json", "rb"))


@dp.callback_query_handler(text_startswith="resultXslx:")
async def get_json_result(call: CallbackQuery):
    userAndQuery = call.data[11:]
    additional_path_ = f"\{str(userAndQuery).split(':')[0]}\{str(userAndQuery).split(':')[1]}"
    await bot.send_document(chat_id=call.from_user.id, document=open(BASE_DIR + additional_path_ + r"\result.xlsx", "rb"))

'''
@dp.callback_query_handler(text_startswith="resultPdf:")
async def get_json_result(call: CallbackQuery):
    userAndQuery = call.data[10:]
    additional_path_ = f"\{str(userAndQuery).split(':')[0]}\{str(userAndQuery).split(':')[1]}"
    await bot.send_document(chat_id=call.from_user.id, document=open(BASE_DIR + additional_path_ + r"\result.pdf", "rb"))
   ''' 

@dp.callback_query_handler(text_startswith="resultTxt:")
async def get_json_result(call: CallbackQuery):
    userAndQuery = call.data[10:]
    additional_path_ = f"\{str(userAndQuery).split(':')[0]}\{str(userAndQuery).split(':')[1]}"
    await bot.send_document(chat_id=call.from_user.id, document=open(BASE_DIR + additional_path_ + r"\result.txt", "rb"))


    

async def configurate_result_board(user_name, query):
    json_result = InlineKeyboardButton(text=".json📑", callback_data=f"resultJson:{user_name}:{query}")
    exel_result = InlineKeyboardButton(text=".xslx🗓", callback_data=f"resultXslx:{user_name}:{query}")
    pdf_result = InlineKeyboardButton(text=".pdf🖼", callback_data=f"resultPdf:{user_name}:{query}")
    txt_result = InlineKeyboardButton(text=".txt📝", callback_data=f"resultTxt:{user_name}:{query}")
    return InlineKeyboardMarkup(row_width=2).add(
        json_result, exel_result,
        txt_result, #pdf_result
    )