import asyncio
import json
from playwright.async_api import async_playwright
from collections import namedtupple
import random
from bs4 import BeautifulSoup
import re


class Parser():
    def __init__(self, method:str, query:str) -> None:
        self.method = method
        self.query = query
        
    async def enject_all_data(self):
        try:
            print("qw")
            async with async_playwright() as p:
                context_options = await Parser.queryContextBuilder()
                self.browser = await p.chromium.launch()
                self.context = await self.browser.new_context(**context_options)
                page = await self.context.new_page()
                await asyncio.sleep(0.2)
                url = await Parser.queryUrlBuilder(self.query)
                print(url)
                await page.goto(url=url)
                await asyncio.sleep(0.2)
                await page.screenshot(path="example.png")
                result = await page.content()
                with open(file="result.html", mode="+a", encoding="utf-8" ) as file:
                    file.writelines(result)
                return await Parser.handlerResponce(result)
        except Exception as e:
            print(e)
    
    @staticmethod
    async def queryUrlBuilder(q:str) -> str:
        return f"https://megamarket.ru/catalog/?q={q}"
    

    @staticmethod
    async def queryContextBuilder() -> dict:
        return {
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
                    "is_mobile": True,
                    "java_script_enabled": True
            }

    @staticmethod
    async def handlerResponce(html:str):
        try:
            soup = BeautifulSoup(html, "html.parser")
            links = soup.find_all("a", class_="ddl_product_link")

            for link in links:
                print(link.text, link["href"])
        except Exception as err:
            print(err)



async def  main():
    print("w")
    parser = Parser(method="method", query="Iphone15")
    await parser.enject_all_data()

asyncio.run(main())