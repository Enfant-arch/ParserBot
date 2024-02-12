import re
from playwright.async_api import async_playwright
from playwright._impl._errors import TimeoutError
import json
import asyncio
import random
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


Main_catalog = InlineKeyboardMarkup(row_width=2)




pattern0 = r"window\.__APP__=(\{.*?\});"
pattern = r'"currentDepartmentCategories"\s*:\s*(\[(?:[^\[\]]|\[(?:[^\[\]]|\[[^\[\]]*\])*\])*\])'
context =  {
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
                    "is_mobile": False,
                    "viewport" : {'width':random.randint(1090,1099), 'height':738},
                    "java_script_enabled": True
            }

async def enject_catalog():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context_parsing = await browser.new_context(**context)
        page = await context_parsing.new_page()
        asyncio.sleep(1)
        await page.goto("https://megamarket.ru/catalog/")
        html = await page.content()
        match = re.findall(pattern0, html, re.DOTALL)
        if match:
            catalog = re.search(pattern, match[1])
            return catalog.group(1)
        else: return None

async def keyboard_buttons():
    catalog_data = await enject_catalog()
    print(catalog_data)