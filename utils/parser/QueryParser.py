import asyncio
import json
from playwright.async_api import async_playwright
from playwright._impl._errors import TimeoutError
import random
from bs4 import BeautifulSoup
import lxml
from datetime import datetime
from utils.parser.Good import Good
from admin_panel.panel.core import core
from utils.parser.ResultBuilder import ResultBuilder
import re

import time

base_path = "https://megamarket.ru/"



class Parser():
    def __init__(self, query:str, is_mobile=False, page=0) -> None:
        self.page = page
        self.query = query.replace("-", "%20")
        self.htmlResponce = None
        self._products = Good()
        self.context = None
        self.IsMoblie = is_mobile
        self.url =  Parser.queryUrlBuilder(self.page, self.query)
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
                core.logger.make_log(self.url)
                await page.goto(url=self.url)
                await asyncio.sleep(2)
                await page.keyboard.down("End")

                self.url = await Parser.queryUrlProccesing(page.url, self.page, self.query)
                self.htmlResponce = await page.content()

        except TimeoutError as err:
            core.logger.make_log(err)
            return TimeoutError
        
    
    async def dispose(self):
        await self.context_parsing.close()
        await self.browser.close()
    
    

    async def handlerResponce(self):
        try:
            
            soup = BeautifulSoup(self.htmlResponce, "lxml")
            results = soup.find_all("div", class_= self.dll)
            for dirtyProductHTML in results:
                dirtyProduct = BeautifulSoup(str(dirtyProductHTML), "lxml")
                if self.IsMoblie is False:
                    bonusPercent = dirtyProduct.find("span", class_='bonus-percent')
                    if (bonusPercent is not None):
                        bonusPercent = bonusPercent.get_text().replace("%", "")
                        if(int(bonusPercent)) >= 5:
                            bonusPercent = bonusPercent + "%"
                            bonusPrice  = dirtyProduct.find("span", class_='bonus-amount').get_text().replace("\t","").replace("\n","") + "₽"
                            priceGood = dirtyProduct.find("div", class_="item-price").get_text().replace("\t","").replace("\n","")
                            nameGood = str(dirtyProduct.find("div", class_="item-title").get_text()).replace("\t","").replace("\n","")
                            imageGood = dirtyProduct.find("img", class_="lazy-img")['src']
                            linkGood = base_path + dirtyProduct.find("a", class_="item-image-block ddl_product_link")['href']
                            sellerOfGood = dirtyProduct.find("div", class_="merchant-info__name").get_text()
                            reviewGood = dirtyProduct.find("div", class_ = "review-amount").get_text().replace("\t","").replace("\n","")
                            core.logger.make_log(f"|{nameGood}|||{linkGood}|||{priceGood}|||{bonusPercent}|||{bonusPrice}|||{imageGood}|||{reviewGood}|\n\n\n")
                            self._products.__add__(name=nameGood, link=linkGood, image_link=imageGood, price=priceGood, 
                                        bonusAmount=bonusPrice,  bonusPercent=bonusPercent, reviewCount=reviewGood, seller=sellerOfGood)

        except Exception as err:
            core.logger.make_log(err)
    

    async def queryContextBuilder(self) -> dict:
        self.context =  {
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
                    "is_mobile": False,
                    "viewport" : self.screen,
                    "java_script_enabled": True
            }
        
    @staticmethod
    def queryUrlBuilder(page, query) -> str: 
        if page > 0:
            return f"{base_path}catalog/page-{page}/?q={query}/"
        elif page == 0:
            return f"{base_path}catalog/?q={query}"
        
    @staticmethod
    async def queryUrlProccesing(url, page, query) -> str: 
        pattern = re.compile(f"{base_path}catalog/"+ "(.+?)/")
        match = pattern.search(url)
        if match:
            if match.group(1).startswith("page") == False: return f"{base_path}catalog/{match.group(1)}/page-{page}/#?related_search={match.group(1)}"
        else: 
            if page > 0 : return f"{base_path}catalog/page-{page}/?q={query}/"
            elif page == 0 : return f"{base_path}catalog/?q={query}"




#asyncio.run(main())