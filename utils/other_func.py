# - *- coding: utf- 8 - *-
import asyncio
import datetime
import time

import requests
from aiogram import Dispatcher
from bs4 import BeautifulSoup
from admin_panel.entities.admin import Admin
from data.config import bot_version, bot_description
from loader import bot
from utils.db_api.psql import get_settingsx, update_settingsx, process_timer



async def on_startup_notify(dp: Dispatcher):
    if len(Admin.admins()) >= 1:
        update_link = "https://sites.google.com/view/check-update-autoshop/main-page"

        response = requests.get(update_link)
        soup_parse = BeautifulSoup(response.text, "html.parser")
        get_bot_info = soup_parse.select("span[class$='C9DxTc']")[0].text.split("=")
        if float(get_bot_info[0].replace("^", "", 5)) <= float(bot_version):
            await send_all_admin(f"<b>✅ Бот был успешно запущен</b>\n"
                                 f"➖➖➖➖➖➖➖➖➖➖\n"
                                 f"{bot_description}")
        else:
            update_description = get_bot_info
            update_description = "\n".join(update_description)
            await send_all_admin(f"<b>✅ Бот был успешно запущен</b>\n"
                                 f"➖➖➖➖➖➖➖➖➖➖\n"
                                 f"{bot_description}\n"
                                 f"➖➖➖➖➖➖➖➖➖➖\n"
                                 f"<b>❇ Вышло обновление ❇</b>\n"
                                 f"▶ <a href='{get_bot_info}'><b>Скачать обновление</b></a>\n"
                                 f"➖➖➖➖➖➖➖➖➖➖\n"
                                 f"{update_description}")


async def send_all_admin(message, markup=None, not_me=0):
    if markup is None:
        for admin in Admin.admins():
            try:
                if str(admin) != str(not_me):
                    await bot.send_message(admin, message, disable_web_page_preview=True)
            except:
                pass
    else:
        for admin in Admin.admins():
            try:
                if str(admin) != str(not_me):
                    await bot.send_message(admin, message, reply_markup=markup, disable_web_page_preview=True)
            except:
                pass


# Очистка имени пользователя от тэгов
def clear_firstname(firstname):
    if "<" in firstname: firstname = firstname.replace("<", "")
    if ">" in firstname: firstname = firstname.replace(">", "")
    return firstname

def validate_folder_name(string):
    if not string:return False
    invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in invalid_chars:
        if char in string: return False

    reserved_words = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']
    if string.upper() in reserved_words:return False
    return True

def make_folder_name(string):
    invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', " "]
    for char in invalid_chars:
        string = string.replace(char, '-')
    return string


# Проверка на обновление счётчика 24-х часов при запуске
def update_profit():
    settings = get_settingsx()
    now_unix = int(time.time())
    if now_unix - int(settings[4]) >=86400:
        update_settingsx(profit_buy=now_unix)
    if now_unix - int(settings[5]) >= 86400:
        update_settingsx(profit_refill=now_unix)


# Автоматическая ежечасовая проверка на обновление счётчика 24-х часов
async def update_last_profit():
    while True:
        await asyncio.sleep(3600)
        settings = get_settingsx()
        now_unix = int(time.time())
        if now_unix - int(settings[4]) >= 86400:
            update_settingsx(profit_buy=int(now_unix))
        if now_unix - int(settings[5]) >= 86400:
            update_settingsx(profit_refill=now_unix)

async def update_notifical_payment():
    while True:
        await process_timer()
        await asyncio.sleep(600)
        
import re
import json
import asyncio
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from collections import namedtuple

{"id":"Z385079901903_Z901903688511",
"title":"Столы для ноутбука","titleImage":"https:\u002F\u002Fmain-cdn.sbermegamarket.ru\u002Fmid9\u002Fhlr-system\u002F189\u002F800\u002F082\u002F662\u002F022\u002F36\u002F2463684633829567t.jpg","nodes":[],"sequence":11000,
"subTitle":"","category":None,"collection":
{"collectionId":"688511","parentId":"901903","collectionType":"CATEGORY","title":"Столы для ноутбука","isDepartment":False,"hierarchy":[],"url":"\u002Fcatalog\u002Fstoly-dlya-noutbuka\u002F",
"images":{},"description":"","slug":"stoly-dlya-noutbuka","navigationMode":"","allowedServiceSchemes":[],"code":"","mainListingCollectionId":"",
"attributes":None,"rating":{},"shortTitle":"","mainListingCollectionRelativeUrl":"",
"name":"","displayName":""}
,"parentId":"Z385079901903"}
catalog_entity = namedtuple("Position", ["id", "title", "titleImage", "nodes",
                "sequence","subTitle", "category", "collection", "parentId"])

f = open(file=r"C:\Users\frigm\Desktop\Mega\ParserBot\page.html", mode="r+", encoding='utf-8')

catalog_list = list()
Main_catalog = InlineKeyboardMarkup(row_width=2)
html = f.read()


pattern0 = r"window\.__APP__=(\{.*?\});"
pattern = r'"currentDepartmentCategories"\s*:\s*(\[(?:[^\[\]]|\[(?:[^\[\]]|\[[^\[\]]*\])*\])*\])'
async def test_enject():
    match = re.findall(pattern0, html, re.DOTALL)
    if match:
        catalog = re.search(pattern, match[1])
        return str(catalog.group(1)).replace("null", "None").replace("false", "False").replace("true", "True")
    else:
        print("Не нашли currentDepartmentCategories")

async def test_kbB():
    data = await test_enject()
    #callbackdata = "item:id:parentid"
    catalog_list = eval(data)
    for item in catalog_list:
        if str(item["parentId"]) == "0":
            Main_catalog.add(InlineKeyboardButton(text=item["title"], callback_data=f"catalog_item:{item['id']}"))

    
    


# Автоматическая проверка обновления каждые 24 часа
async def check_update_bot():
    while True:
        await asyncio.sleep(86400)
        update_link = "https://sites.google.com/view/check-update-autoshop/main-page"

        response = requests.get(update_link)
        soup_parse = BeautifulSoup(response.text, "html.parser")
        get_bot_info = soup_parse.select("p[class$='CDt4Ke zfr3Q']")[0].text.split("=")
        if float(get_bot_info[0]) > float(bot_version):
            update_description = get_bot_info[2].split("**")
            update_description = "\n".join(update_description)
            await send_all_admin(f"<b>❇ Вышло обновление ❇</b>\n"
                                 f"▶ <a href='{get_bot_info[1]}'><b>Скачать обновление</b></a>\n"
                                 f"➖➖➖➖➖➖➖➖➖➖\n"
                                 f"{update_description}")

# Получение текущей даты
def get_dates():
    return datetime.datetime.today().replace(microsecond=0)






