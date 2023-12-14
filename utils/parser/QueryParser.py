import asyncio
import json
from playwright.async_api import async_playwright
import random
from bs4 import BeautifulSoup
import re


class Parser():
    def __init__(self, method:str, query:str) -> None:
        self.method = method
        self.query = query
        
    async def enject_all_data(self):
        try:
            async with async_playwright() as p:
                context_options = await Parser.queryContextBuilder()
                self.browser = await p.chromium.launch()
                self.context = await self.browser.new_context(**context_options)
                page = await self.context.new_page()
                await asyncio.sleep(0.2)
                url = await Parser.queryUrlBuilder(self.query)
                print(url)
                await page.goto(url=url)
                await asyncio.sleep(0.6)
                await page.screenshot(path="example.png")
                result = await page.content()
                with open("result.html", "+a") as file:
                    file.writelines(result)
                return await Parser.handlerResponce(result)
        except Exception as e:
            return e
    
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
            doc = BeautifulSoup(html, "html.parser")
            script_tag = doc.find("script", string=re.compile("window.__APP__"))
            print(script_tag)
            script_data = script_tag.string.strip()
            cfg_data = re.search(r'"cfg":(.+?)}', script_data).group(1)
        except Exception as err:
            print(err)



async def  main():
    parser = Parser(method="method", query="Айфон 15")
    await parser.enject_all_data()

asyncio.run(main())