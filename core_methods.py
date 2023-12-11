
import hashlib
import sqlite3
from bs4 import BeautifulSoup

import requests


path_to_db = "data/botBD.sqlite"
Min_Pay = 5
TOKEN  = "6845863329:AAEgTN2Sk1SZW1PxagN7_oP18n8Sb2B3pE0"
API_KEY = "62b29a31b8-68bbc4e456-048275e8d6-65630b4769"
to_val = "RUB"
sending  = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
sending_stiker = f'https://api.telegram.org/bot{TOKEN}/sendSticker'

def confirm_pay(address, amount, currency, txid):
    id = get_id(address=address)
    if id is None:
        send_notification_tg(6094743728, f"201\n\nПроизошла ошибка!\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t***✅ТРАНЗАКЦИЯ ОСУЩЕСТВЛЕННА 🆗***\n\nНо время ожидания в боте прошло, и транзакция имела статус отмененой(status=1) \n\n ***Amount*** : `{amount}{currency}`\n\n`{address}`")
        return
    amountToVal = currency_converter(amount=amount, from_val=currency)
    print(amountToVal)
    update_balance(id[0], amountToVal)
    update_status(id[0], address)
    send_notification_tg(id[0], f"✅***Ваш*** баланс пополнен на `{amountToVal}{to_val}`!\nID транзакции : `{txid}`")
    x = send_sticker_tg(id[0], r"CAACAgIAAxkBAAEKzoVlX6fG1a-FwenpqBExEKNTO8lVxgACqwADO2AkFLRQgMz3RrqdMwQ")   
    print(x)



def cancel_pay(address, sign, currency, amount):
    id = get_id(address=address)
    if(id is None):
        send_notification_tg(6094743728, f"Пришла оплата на пустой адресс : `{address}`\n\n***Sign***:`{sign}` \n\n ***Amount*** :`{amount}{currency}`")
        return
    else:
        send_notification_tg(id[0], f"Произошла ошибка с подверждением вашей транзакции записи не соответсвуют\nПросьба обратиться в службу поддержки***Sign***:`{sign}` \n\n ***Amount*** :`{amount}{currency}`")












def verify_signature(data):
    if int(data['cryptocurrencyapi.net']) < 3:
        return False, 'Request does not meet the minimum criteria'

    sign0 = data['sign']
    if sign0 is None:
        return 1404, 'Sign missing'
    
    data.pop('sign', None)

    sorted_keys = sorted(data.keys())
    values_str = ':'.join(str(data[key]) for key in sorted_keys)

    hashed_api_key = hashlib.md5(API_KEY.encode('utf-8')).hexdigest()
    sign = hashlib.sha1((values_str + ':' + hashed_api_key).encode('utf-8')).hexdigest()
    print(sign)
    if sign != sign0:
        return 1405, str(sign)
    else:
        return 1200, 'OK'



def currency_converter(amount, from_val:str):
    url = f"https://www.xe.com/currencyconverter/convert/?Amount={amount}&From={from_val.upper()}&To={to_val.upper()}"
    responce = requests.get(url, headers={'User-Agent' : "Magic Browser"}) 
    result = responce.text
    soup = BeautifulSoup(result, "html.parser")
    price = soup.find("p", class_ = "result__BigRate-sc-1bsijpp-1 dPdXSB")
    recycle  = str(price).split('result__BigRate-sc-1bsijpp-1 dPdXSB">')
    price = recycle[1].split('<!-- -->')
    return price[0].split("<span")[0].replace(",","")





def update_balance(user_id, amount):
    with sqlite3.connect(path_to_db) as db:
        check_sql = db.execute(f"UPDATE storage_users SET balance = balance + {float(amount)} WHERE user_id = {user_id}")

def update_status(user_id, address):
    with sqlite3.connect(path_to_db) as db:
        check_sql = db.execute(f"UPDATE storage_crypto_payment SET status = 1 WHERE user_id = {user_id} and  address = '{address}'")

def send_notification_tg(user_id: int, message:str) -> requests.Response:
    query_params = {
        "chat_id" : user_id,
        "text" : message,
        "parse_mode" : "markdown",
    }
    response = requests.get(url=sending, params=query_params)
    return response.text

def send_sticker_tg(user_id: int, sticker_id:str) -> requests.Response:
    query_params = {
        "chat_id" : user_id,
        "sticker" : sticker_id,
    }
    response = requests.get(url=sending_stiker, params=query_params)
    return response.text

def get_id(**kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = f"SELECT user_id FROM storage_crypto_payment WHERE status = 0 AND "
        sql, parameters = get_format_args(sql, kwargs)
        get_response = db.execute(sql, parameters)
        get_response = get_response.fetchone()
        return get_response









def update_format_with_args(sql, parameters: dict):
    values = ", ".join([
        f"{item} = ?" for item in parameters
    ])
    sql = sql.replace("XXX", values)
    return sql, tuple(parameters.values())



def get_format_args(sql, parameters: dict):
    sql += " AND ".join([
        f"{item} = ?" for item in parameters
    ])
    return sql, tuple(parameters.values())



def add_userx(user_id, user_login, user_name, balance, all_refill, reg_date):
    with sqlite3.connect(path_to_db) as db:
        db.execute("INSERT INTO storage_users "
                   "(user_id,  user_login, user_name, balance, all_refill, reg_date, payment_address, wait_pay ) "
                   "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   [user_id, user_login, user_name, balance, all_refill, reg_date, "", False])
        db.commit()


# Изменение пользователя
def update_userx(user_id, **kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = f"UPDATE storage_users SET XXX WHERE user_id = {user_id}"
        sql, parameters = update_format_with_args(sql, kwargs)
        db.execute(sql, parameters)
        db.commit()
