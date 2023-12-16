import asyncio
import json
from playwright.async_api import async_playwright
from playwright._impl._errors import TimeoutError
import random
from bs4 import BeautifulSoup
import lxml
from datetime import datetime
from Good import product
import re
import time




class Parser():
    def __init__(self, method:str, query:str) -> None:
        self.method = method
        self.query = query
        self.htmlResponce = None
        self._products = None
        
    async def enject_all_data(self):
        try:
            async with async_playwright() as p:
                context_options = await Parser.queryContextBuilder()
                self.browser = await p.chromium.launch()
                self.context = await self.browser.new_context(**context_options)
                page = await self.context.new_page()
                url = await Parser.queryUrlBuilder(self.query)
                print(url)
                await page.goto(url=url)
                await asyncio.sleep(0.2)
                await page.keyboard.down("End")
                await asyncio.sleep(0.2)
                await page.screenshot(path="example.png")
                result = await page.content()
                self.htmlResponce = result
                with open(file="result.html", mode="+a", encoding="utf-8" ) as file:
                    file.writelines(result)
                await self.context.close()
                await self.browser.close()
                return await Parser.handlerResponce(result)

        except TimeoutError as err:
            print(err)
            return err
    
    @staticmethod
    async def queryUrlBuilder(q:str) -> str:
        return f"https://megamarket.ru/catalog/?q={q}"
    

    @staticmethod
    async def queryContextBuilder() -> dict:
        return {
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
                    "is_mobile": True,
                    "viewport" : {'width':818, 'height':693},
                    "java_script_enabled": True
            }

    @staticmethod
    async def handlerResponce(html:str):
        try:
            soup = BeautifulSoup(html, "lxml")
            results = soup.find_all("div", class_="catalog-item-mobile ddl_product")
            for dirtyProductHTML in results:
                print(dirtyProductHTML)
                dirtyProduct = BeautifulSoup(str(dirtyProductHTML), "lxml")
                name  = dirtyProduct.find("a", class_='dll_product_link')
                print(name)
        except Exception as err:
            print(err)



async def  main():
    start = datetime.now()
    parser = Parser(method="method", query="Iphone15")
    await parser.enject_all_data()
    end = datetime.now()
    print((end - start))

asyncio.run(main())