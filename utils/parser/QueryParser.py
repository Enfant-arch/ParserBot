import asyncio
import json
from playwright.async_api import async_playwright
from playwright._impl._errors import TimeoutError
import random
from bs4 import BeautifulSoup
import lxml
from datetime import datetime
from utils.parser.Good import Good
from utils.parser.ResultBuilder import ResultBuilder
import re

import time

base_path = "https://megamarket.ru/"


class Parser():
    def __init__(self, query:str, is_mobile=False, page=0) -> None:
        self.page = page
        self.query = query
        self.htmlResponce = None
        self._products = Good()
        self.context = None
        self.IsMoblie = is_mobile
        if self.IsMoblie is False:
            self.dll = "catalog-item catalog-item-desktop ddl_product"
            self.screen = {'width':random.randint(1201,1208), 'height':738}
        else:
            self.screen = {'width':random.randint(1090,1099), 'height':738}
            self.dll = "catalog-item-mobile ddl_product"
        
    async def enject_all_data(self):
        try:
            async with async_playwright() as p:
                self.browser = await p.chromium.launch()
                
                self.context_parsing = await self.browser.new_context(**self.context)
                page = await self.context_parsing.new_page()
                url = await Parser.queryUrlBuilder(self.query)
                await page.goto(url=url)
                await page.keyboard.down("End")
                await page.screenshot(path="example.png")
                self.htmlResponce = await page.content()

        except TimeoutError as err:
            print(err)
        except Exception as err:
            print(err)
    
    async def dispose(self):
        await self.context_parsing.close()
        await self.browser.close()
    
    
    async def queryContextBuilder(self) -> dict:
        self.context =  {
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
                    "is_mobile": False,
                    "viewport" : self.screen,
                    "java_script_enabled": True
            }

    async def handlerResponce(self):
        try:
            soup = BeautifulSoup(self.htmlResponce, "lxml")
            results = soup.find_all("div", class_= self.dll)

            for dirtyProductHTML in results:
                dirtyProduct = BeautifulSoup(str(dirtyProductHTML), "lxml")
                if self.IsMoblie is False:
                    bonusPercent = dirtyProduct.find("span", class_='bonus-percent')
                    if ((bonusPercent != None) and (int(bonusPercent.get_text().replace("%", "")))):
                        bonusPercent = bonusPercent.get_text()
                        bonusPrice  = dirtyProduct.find("span", class_='bonus-amount').get_text().replace("\t","").replace("\n","")
                        priceGood = dirtyProduct.find("div", class_="item-price").get_text().replace("\t","").replace("\n","")
                        nameGood = str(dirtyProduct.find("div", class_="item-title").get_text()).replace("\t","").replace("\n","")
                        imageGood = dirtyProduct.find("img", class_="lazy-img")['src']
                        linkGood = base_path + dirtyProduct.find("a", class_="item-image-block ddl_product_link")['href']
                        reviewGood = dirtyProduct.find("div", class_ = "review-amount").get_text().replace("\t","").replace("\n","")

                        (f"|{nameGood}|||{linkGood}|||{priceGood}|||{bonusPercent}|||{bonusPrice}|||{imageGood}|||{reviewGood}|\n\n\n")
                        self._products.__add__(name=nameGood, link=linkGood, price=priceGood, bonusAmount=bonusPrice, bonusPercent=bonusPercent)

        except Exception as err:
            print(err)
    
    async def show_result(self):
        print(len(self._products))
        for product in self._products:
            print(product)

    async def queryUrlBuilder(self) -> str: 
        if self.page > 0:
            return f"{base_path}catalog/page-{self.page}/?q={self.query}"
        elif self.page == 0:
            return f"{base_path}catalog/?q={self.query}"


#asyncio.run(main())