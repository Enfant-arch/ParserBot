from flask import Flask, jsonify, request, abort
import requests
from core_methods import *
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
ALLOWED_IPS = ['88.99.198.205', '162.159.193.5']




@app.route('/', methods=['POST', "GET"])
def accept_payment():
    data = request.get_json()
    app.logger.info(data)
    type = data["type"]

    if type == "in":
        amount = data["amount"]
        address = data["to"]
        txid = data["txid"]
        chain = data["chain"]
        currency = data["currency"]
        valid, sign = verify_signature(data)

        if valid == 1405:
            cancel_pay(address=address, sign=sign, currency=currency, amount=amount)
            return "bad"
        
        if valid == 1200:
            confirm_pay(address=address,amount=amount, currency=currency, txid=txid)
            return "good"
        
        else:
            return 404
        
    return "ok"



#другое

if not app.debug:
    app.logger.setLevel(logging.INFO)
    # создаем файловый обработчик логгирования 
    handler = RotatingFileHandler('core.log', maxBytes=10000, backupCount=3)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

#примеры запросов
{"cryptocurrencyapi.net":3,"chain":"bitcoin","currency":"BTC","type":"in","date":1700496015,"from":"","to":"184RYTNqaKfjpiJFsLB86WzpH54ANYBhAX","amount":"0.00012958","fee":"0","txid":"9e711693243a2d82393eeecf8b6a1cbafc38da018a396619ef047d9443911899","pos":0,"confirmation":100,"label":"ukrzcbin","sign":"6d86ff885fd2728f89f5a96cec3093df1b84affe"}
{"cryptocurrencyapi.net":3,"chain":"ethereum","currency":"ETH","type":"in","date":1700499332,"from":"","to":"0x6c0e785891d348b1a68192577436c500f0159830","token":"","tokenContract":"","amount":"2131","fee":"0","txid":"0x9e711693243a2d82393eeecf8b6a1cbafc38da018a396619ef047d9443911899","pos":0,"confirmation":100,"label":"eirrrnbn","sign":"897037b1e3077470d0ac841456f6f4f48f1e19d9"}
{"cryptocurrencyapi.net":3,"chain":"tron","currency":"TRX","type":"in","date":1700499876,"from":"","to":"TNa9jtsm562exGYTrNGGFyzVGw3T5QhJJY","token":"","tokenContract":"","amount":"1001","fee":"0","txid":"9e711693243a2d82393eeecf8b6a1cbafc38da018a396619ef047d9443911899","pos":0,"confirmation":100,"label":"","sign":"1fc7209d820eb56ec5917811f1784221622df82f"}
{"cryptocurrencyapi.net":3,"chain":"bitcoin","currency":"BTC","type":"error","date":1700497224,"code":"node_insufficient_funds","message":"Insufficient funds","labels":{"6778":"manually"},"ids":[6778],"sign":"9667e462fdc2378fd0800d77238cf9e20712f008"}


@app.before_request
def limit_remote_addr():
    if request.remote_addr not in ALLOWED_IPS:
        abort(403)




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
