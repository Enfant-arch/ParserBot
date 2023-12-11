import asyncio
import json
import requests
import aiohttp
import logging
import random
import string
from utils.payment.env import api_key, HOST, curr
import re
from bs4 import BeautifulSoup


api = api_key
BASE_URL = "https://new.cryptocurrencyapi.net/api/"


"{'cryptocurrencyapi.net': 2, 'currency': 'BTC', 'type': 'in', 'date': 1671646496, 'address': '1A3GWmsqQjgTEphcGFfE52fLnT5jbvKyse', 'amount': '0.00005942', 'txid': 'e162554cc69e5c7c1ee8a1d13ad17de44b4539f9fa137d1cf06f74468eeb7847', 'pos': '0', 'confirmations': '3', 'tag': 'fciuiscm', 'sign': '458e6b06fff21c3b55cb03a674cbe827a5c928c9', 'sign2': '4974aee854a00b3522d4f375df70d5520602a4e6'}"



class CurrencyPayment():


    @property
    async def balance(currency:str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{BASE_URL}{currency}/.balance?key={api}") as response:
                return await response.text(encoding="utf-8")


    @staticmethod
    async def create_wallet(currency:str):
        tag = await CurrencyPayment.generate_random_string(8)
        url = f"{BASE_URL}{currency}/.give?key={api}&period=45&label={tag}"
        logging.info(url)
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as response:
                to_json = await response.text(encoding="utf-8")
                logging.info(to_json)
                json_object = json.loads(to_json)
                return json_object["result"]
            

    @staticmethod
    async def tracking(currency:str, address, amount):
        async with aiohttp.ClientSession() as session:
            tag = await CurrencyPayment.generate_random_string(8)
            async with session.get(f"{BASE_URL}{currency}.track?key={api}&address={address}&amount={amount}&tag={tag}&lifetime=30&statusURL=http://{HOST}") as response:
                return await response.text(encoding="utf-8")
            

    @staticmethod
    async def send_coins(currency:str, amount, addres):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{BASE_URL}{currency}.send?key={api}&to={addres}&amount={amount}&statusURL=http://{HOST}") as response:
                return await response.text(encoding="utf-8")



    @staticmethod
    async def status(currency:str, id):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{BASE_URL}{currency}.status?key={api}&id={id}") as response:
                return await response.json(encoding="utf-8")
            

            
    @staticmethod
    async def currency_converter(amount, from_val:str, to_val:str):
        async with aiohttp.ClientSession() as session:
            url = f"https://www.xe.com/currencyconverter/convert/?Amount={amount}&From={from_val.upper()}&To={to_val.upper()}"
            async with session.get(url, headers={'User-Agent' : "Magic Browser"}) as response: 
                result = await response.text(encoding="utf-8")
                soup = BeautifulSoup(result, "html.parser")
                price = soup.find("p", class_ = "result__BigRate-sc-1bsijpp-1 dPdXSB")
                recycle  = str(price).split('result__BigRate-sc-1bsijpp-1 dPdXSB">')
                price = recycle[1].split('<!-- -->')
                return price[0]
    

    @staticmethod
    async def generate_random_string(length:int) -> str:
        letters = string.ascii_lowercase
        RandomString = ''.join(random.choice(letters) for i in range(length))
        return RandomString

