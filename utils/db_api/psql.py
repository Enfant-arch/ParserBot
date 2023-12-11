# - *- coding: utf- 8 - *-
import datetime
import logging
import random
import psycopg2
import time
import asyncio
from aiogram.types import ParseMode
from loader import dp, bot
from data.config import bot_description
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.fields import BaseField


connection = psycopg2.connect(
    database="megamarket",
    host='localhost',
    user='postgres',
    password='root',
    port='5432'
)  
connection.autocommit = True
sem = asyncio.Semaphore(80)

cursor = connection.cursor()



###payment_notification
async def process_timer():
    pass    




def logger(statement):
    logging.basicConfig(
        level=logging.INFO,
        filename="logs.log",
        format=f"[Executing] [%(asctime)s] | [%(filename)s LINE:%(lineno)d] | {statement}",
        datefmt="%d-%b-%y %H:%M:%S"
    )
    logging.info(statement)


def handle_silently(function):
    def wrapped(*args, **kwargs):
        result = None
        try:
            result = function(*args, **kwargs)
        except Exception as e:
            logger("{}({}, {}) failed with exception {}".format(
                function.__name__, repr(args[1]), repr(kwargs), repr(e)))
        return result

    return wrapped


####################################################################################################
###################################### ФОРМАТИРОВАНИЕ ЗАПРОСА ######################################
# Форматирование запроса с аргументами
def update_format_with_args(sql, parameters: dict):
    values = ", ".join([
        f"{item} = ?" for item in parameters
    ])
    sql = sql.replace("XXX", values)
    return sql, tuple(parameters.values())


# Форматирование запроса без аргументов
def get_format_args(sql, parameters: dict):
    sql += " AND ".join([
        f"{item} = ?" for item in parameters
    ])
    return sql, tuple(parameters.values())


####################################################################################################
########################################### ЗАПРОСЫ К БД ###########################################
# Добавление пользователя
def add_userx(user_id, user_login, user_name, balance, all_refill, reg_date):
    cursor.execute("INSERT INTO storage_users "
                "(user_id,  user_login, user_name, balance, all_refill, reg_date ) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                [user_id, user_login, user_name, balance, all_refill, reg_date])
    cursor.commit()


# Изменение пользователя
def update_userx(user_id, **kwargs):
    sql = f"UPDATE storage_users SET XXX WHERE user_id = {user_id}"
    sql, parameters = update_format_with_args(sql, kwargs)
    cursor.execute(sql, parameters)
    cursor.commit()



def delete_userx(**kwargs):
    sql = "DELETE FROM storage_users WHERE "
    sql, parameters = get_format_args(sql, kwargs)
    cursor.execute(sql, parameters)
    cursor.commit()


# Получение пользователя
def get_userx(**kwargs):
    sql = "SELECT * FROM storage_users WHERE "
    sql, parameters = get_format_args(sql, kwargs)
    get_response = cursor.execute(sql, parameters)
    get_response = get_response.fetchone()
    return get_response


# Получение пользователей
def get_usersx(**kwargs):
    sql = "SELECT * FROM storage_users WHERE "
    sql, parameters = get_format_args(sql, kwargs)
    get_response = cursor.execute(sql, parameters)
    get_response = get_response.fetchall()
    return get_response


# Получение всех пользователей
def get_all_usersx():
    get_response = cursor.execute("SELECT * FROM storage_users")
    get_response = get_response.fetchall()
    return get_response


# Получение платежных систем
def get_paymentx():
    get_response = cursor.execute("SELECT * FROM storage_payment")
    get_response = get_response.fetchone()
    return get_response




# Изменение платежных систем
def update_paymentx(**kwargs):
    sql = f"UPDATE storage_payment SET XXX "
    sql, parameters = update_format_with_args(sql, kwargs)
    cursor.execute(sql, parameters)
    cursor.commit()

def add_payment_crypto(user_id, address, user_login, currency, expect_value):
    cursor.execute("INSERT INTO storage_crypto_payment (" \
                    "address , user_id," \
                    "user_login , status , " \
                    "currency, except_value, unix_time) " \
                    "VALUES (?, ?, ?, ?, ?, ?, ?)",
                [ address, user_id, user_login, False, currency, expect_value, time.time() + 86400])
    cursor.commit()



# Изменение платежа
def update_payment_crypto(user_id, currency, **kwargs):
    sql = f"UPDATE storage_crypto_payment SET XXX WHERE user_id = {user_id} AND currency = '{currency}'"
    sql, parameters = update_format_with_args(sql, kwargs)
    cursor.execute(sql, parameters)
    cursor.commit()



def get_payment_crypto(user_id, what_select, **kwargs):
    sql = f"SELECT {what_select} FROM storage_crypto_payment WHERE user_id = {user_id} AND status = 0"
    sql, parameters = get_format_args(sql, kwargs)
    get_response = cursor.execute(sql, parameters)
    get_response = get_response.fetchall()
    return get_response



# Получение настроек
def get_settingsx():
    get_response = cursor.execute("SELECT * FROM storage_settings")
    get_response = get_response.fetchone()
    return get_response 



def update_settingsx(**kwargs):
    sql = f"UPDATE storage_settings SET XXX "
    sql, parameters = update_format_with_args(sql, kwargs)
    cursor.execute(sql, parameters)
    cursor.commit()



def add_refillx(user_id, user_login, user_name, comment, amount, receipt, way_pay, dates, dates_unix):
    cursor.execute("INSERT INTO storage_refill "
                "(user_id, user_login, user_name, comment, amount, receipt, way_pay, dates, dates_unix) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                [user_id, user_login, user_name, comment, amount, receipt, way_pay, dates, dates_unix])
    cursor.commit()


# Получение пополнения
def get_refillx(what_select, **kwargs):
    sql = f"SELECT {what_select} FROM storage_refill WHERE "
    sql, parameters = get_format_args(sql, kwargs)
    get_response = cursor.execute(sql, parameters)
    get_response = get_response.fetchone()
    return get_response



def get_refillsx(what_select, **kwargs):
    sql = f"SELECT {what_select} FROM storage_refill WHERE "
    sql, parameters = get_format_args(sql, kwargs)
    get_response = cursor.execute(sql, parameters)
    get_response = get_response.fetchall()
    return get_response


# Получение всех пополнений
def get_all_refillx():
    sql = "SELECT * FROM storage_refill"
    get_response = cursor.execute(sql)
    get_response = get_response.fetchall()
    return get_response


# Добавление категории в БД
def add_categoryx(category_id, category_name):
    cursor.execute("INSERT INTO storage_category "
                "(category_id, category_name) "
                "VALUES (?, ?)",
                [category_id, category_name])
    cursor.commit()


# Изменение категории
def update_categoryx(category_id, **kwargs):
    
        sql = f"UPDATE storage_category SET XXX WHERE category_id = {category_id}"
        sql, parameters = update_format_with_args(sql, kwargs)
        cursor.execute(sql, parameters)
        cursor.commit()


# Получение категории
def get_categoryx(what_select, **kwargs):
    sql = f"SELECT {what_select} FROM storage_category WHERE "
    sql, parameters = get_format_args(sql, kwargs)
    get_response = cursor.execute(sql, parameters)
    get_response = get_response.fetchone()
    return get_response


# Получение категорий
def get_categoriesx(what_select, **kwargs):
    sql = f"SELECT {what_select} FROM storage_category WHERE "
    sql, parameters = get_format_args(sql, kwargs)
    get_response = cursor.execute(sql, parameters)
    get_response = get_response.fetchall()
    return get_response


# Получение всех категорий
def get_all_categoriesx():
    sql = "SELECT * FROM storage_category"
    get_response = cursor.execute(sql)
    get_response = get_response.fetchall()
    return get_response


# Очистка категорий
def clear_categoryx():
    
        sql = "DELETE FROM storage_category"
        cursor.execute(sql)
        cursor.commit()


# Удаление товаров
def remove_categoryx(**kwargs):
    
        sql = "DELETE FROM storage_category WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        cursor.execute(sql, parameters)
        cursor.commit()


# Добавление категории в БД
def add_positionx(position_id, position_name, position_type, position_price,  position_price_day,  position_price_week, position_price_month, position_discription, position_image, position_date,
                  category_id, base_path, path_change):
    
        logging.info("work")
        if position_type == 2:
            cursor.execute("INSERT INTO storage_position "
                   "(position_id, position_name, position_type, position_price, position_price_day, position_price_week, position_price_mounth,  position_discription, position_image, position_date, category_id, base_path, path_change) "
                   "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   [position_id, position_name, position_type, position_price, position_price_day, position_price_week,  position_price_month,  position_discription, position_image,
                    position_date, category_id, base_path, path_change])
        else:
            cursor.execute("INSERT INTO storage_position "
                   "(position_id, position_name, position_type, position_price, position_discription, position_image, position_date, category_id) "
                   "VALUES (?, ?, ?, ?, ?, ?, ?)",
                   [position_id, position_name, position_type, position_price, position_discription, position_image,
                    position_date, category_id])
        cursor.commit()


# Изменение позиции
def update_positionx(position_id, **kwargs):
    
        sql = f"UPDATE storage_position SET XXX WHERE position_id = {position_id}"
        sql, parameters = update_format_with_args(sql, kwargs)
        cursor.execute(sql, parameters)
        cursor.commit()


# Получение категории
def get_positionx(what_select, **kwargs):
    
    sql = f"SELECT {what_select} FROM storage_position WHERE "
    sql, parameters = get_format_args(sql, kwargs)
    get_response = cursor.execute(sql, parameters)
    get_response = get_response.fetchone()
    return get_response




# Получение категорий
def get_positionsx(what_select, **kwargs):
    
    sql = f"SELECT {what_select} FROM storage_position WHERE "
    sql, parameters = get_format_args(sql, kwargs)
    get_response = cursor.execute(sql, parameters)
    get_response = get_response.fetchall()
    return get_response


# Получение всех категорий
def get_all_positionsx():
    
    sql = "SELECT * FROM storage_position"
    get_response = cursor.execute(sql)
    get_response = get_response.fetchall()
    return get_response


# Очистка категорий
def clear_positionx():
    
        sql = "DELETE FROM storage_position"
        cursor.execute(sql)
        cursor.commit()


# Удаление позиций
def remove_positionx(**kwargs):
    
        sql = "DELETE FROM storage_position WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        cursor.execute(sql, parameters)
        cursor.commit()


# Добавление категории в БД
def add_itemx(category_id, position_id, position_type, get_all_items, user_id, user_name):
    
        for item_data in get_all_items:
            if not item_data.isspace() and item_data != "":
                item_id = [random.randint(100000, 999999)]
                cursor.execute("INSERT INTO storage_item "
                           "(item_id, item_data, position_id, position_type, category_id, creator_id, creator_name, add_date) "
                           "VALUES (?, ?, ?, ?, ?, ?, ?)",
                           [item_id[0], item_data, position_id, category_id, user_id, user_name,
                            datetime.datetime.today().replace(microsecond=0)])
        cursor.commit()


# Изменение категории
def update_itemx(item_id, **kwargs):
    
        sql = f"UPDATE storage_item SET XXX WHERE item_id = {item_id}"
        sql, parameters = update_format_with_args(sql, kwargs)
        cursor.execute(sql, parameters)
        cursor.commit()


# Получение категории
def get_itemx(what_select, **kwargs):
    
    sql = f"SELECT {what_select} FROM storage_item WHERE "
    sql, parameters = get_format_args(sql, kwargs)
    get_response = cursor.execute(sql, parameters)
    get_response = get_response.fetchone()
    return get_response


# Получение категорий
def get_itemsx(what_select, **kwargs):
    
    sql = f"SELECT {what_select} FROM storage_item WHERE "
    sql, parameters = get_format_args(sql, kwargs)
    get_response = cursor.execute(sql, parameters)
    get_response = get_response.fetchall()
    return get_response


# Получение всех категорий
def get_all_itemsx():
    
    sql = "SELECT * FROM storage_item"
    get_response = cursor.execute(sql)
    get_response = get_response.fetchall()
    return get_response


# Очистка категорий
def clear_itemx():
    
        sql = "DELETE FROM storage_item"
        cursor.execute(sql)
        cursor.commit()


# Удаление товаров
def remove_itemx(**kwargs):
    
        sql = "DELETE FROM storage_item WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        cursor.execute(sql, parameters)
        cursor.commit()


# Покупка товаров
def buy_itemx(get_items, get_count):
    
    send_count = 0
    save_items = []
    for select_send_item in get_items:
        if send_count != get_count:
            send_count += 1
            save_items.append(f"{send_count}. <code>{select_send_item[2]}</code>")
            sql, parameters = get_format_args("DELETE FROM storage_item WHERE ", {"item_id": select_send_item[1]})
            cursor.execute(sql, parameters)
            split_len = len(f"{send_count}. <code>{select_send_item[2]}</code>")
        else:
            break
        cursor.commit()
    return save_items, send_count, split_len




# Получение всех категорий
def get_licence():
    
    sql = "SELECT * FROM licence_item"
    get_response = cursor.execute(sql)
    get_response = get_response.fetchall()
    return get_response


# Очистка категорий
def clear_licence():
    
        sql = "DELETE FROM licence_item"
        cursor.execute(sql)
        cursor.commit()

def add_licence(hwid, licence_time, user_id, user_login, user_name, receipt, item_count, item_price, item_price_one_item,
                  item_position_id,
                  item_position_name, item_buy, balance_before, balance_after, buy_date, buy_date_unix):
   
        cursor.execute("INSERT INTO licence_purhases "
                   "(HWID,  licence_time, change_times, user_id, user_login, user_name, receipt, item_count, item_price, item_price_one_item, item_position_id, "
                   "item_position_name, item_buy, balance_before, balance_after, buy_date, buy_date_unix) "
                   "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   [ hwid, licence_time, 0, user_id, user_login, user_name, receipt, item_count, item_price, item_price_one_item,
                    item_position_id, item_position_name, item_buy, balance_before, balance_after, buy_date,
                    buy_date_unix])
        cursor.commit()



# Изменение категории
def update_licencex(receipt, **kwargs):
    
        sql = f"UPDATE licence_purhases SET XXX WHERE receipt = '{receipt}'"
        sql, parameters = update_format_with_args(sql, kwargs)
        cursor.execute(sql, parameters)
        cursor.commit()


# Получение категории
def get_licences(what_select, **kwargs):
    
    sql = f"SELECT {what_select} FROM storage_item WHERE "
    sql, parameters = get_format_args(sql, kwargs)
    get_response = cursor.execute(sql, parameters)
    get_response = get_response.fetchone()
    return get_response



# Получение всех категорий
def get_licence():
    
    sql = "SELECT * FROM licence_item"
    get_response = cursor.execute(sql)
    get_response = get_response.fetchall()
    return get_response


# Очистка категорий
def clear_licence():
    
        sql = "DELETE FROM licence_item"
        cursor.execute(sql)
        cursor.commit()


# Удаление товаров
def remove_licence(**kwargs):
    
        sql = "DELETE FROM storage_licence_item WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        cursor.execute(sql, parameters)
        cursor.commit()


# Покупка товаров
def buy_licence(get_items, get_count):
    
    send_count = 0
    save_items = []
    for select_send_item in get_items:
        if send_count != get_count:
            send_count += 1
            save_items.append(f"{send_count}. <code>{select_send_item[2]}</code>")
            split_len = len(f"{send_count}. <code>{select_send_item[2]}</code>")
        else:
            break
    cursor.commit()
    return save_items, send_count, split_len

# Добавление покупки в БД
def add_purchasex(user_id, user_login, user_name, receipt, item_count, item_price, item_price_one_item,
                  item_position_id,
                  item_position_name, item_buy, balance_before, balance_after, buy_date, buy_date_unix):
    
        cursor.execute("INSERT INTO storage_purchases "
                   "(user_id, user_login, user_name, receipt, item_count, item_price, item_price_one_item, item_position_id, "
                   "item_position_name, item_buy, balance_before, balance_after, buy_date, buy_date_unix) "
                   "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   [user_id, user_login, user_name, receipt, item_count, item_price, item_price_one_item,
                    item_position_id, item_position_name, item_buy, balance_before, balance_after, buy_date,
                    buy_date_unix])
        cursor.commit()


# Получение покупки
def get_purchasex(what_select, **kwargs):
    
    sql = f"SELECT {what_select} FROM storage_purchases WHERE "
    sql, parameters = get_format_args(sql, kwargs)
    get_response = cursor.execute(sql, parameters)
    get_response = get_response.fetchone()
    return get_response


# Получение покупок
def get_purchasesx(what_select, **kwargs):
    sql = f"SELECT {what_select} FROM storage_purchases WHERE "
    sql, parameters = get_format_args(sql, kwargs)
    get_response = cursor.execute(sql, parameters)
    get_response = get_response.fetchall()
    return get_response


# Получение всех покупок
def get_all_purchasesx():
    sql = "SELECT * FROM storage_purchases"
    get_response = cursor.execute(sql)
    get_response = get_response.fetchall()
    return get_response


# Последние 10 покупок
def last_licencex(user_id):
    
    sql = "SELECT * FROM licence_purhases WHERE user_id = ? ORDER BY increment DESC LIMIT 10"
    get_response = cursor.execute(sql, [user_id])
    get_response = get_response.fetchall()
    return get_response



def take_more_licence(receipt, user_id):
    sql = "SELECT * FROM licence_purhases WHERE receipt = ? AND user_id = ? ORDER BY increment DESC LIMIT 10"
    get_response = cursor.execute(sql, [receipt, user_id])
    get_response = get_response.fetchall()
    return get_response


def last_purchasesx(user_id):
    sql = "SELECT * FROM storage_purchases WHERE user_id = ? ORDER BY increment DESC LIMIT 10"
    get_response = cursor.execute(sql, [user_id])
    get_response = get_response.fetchall()
    return get_response


# Создание всех таблиц для БД
def create_bdx():
        check_sql = cursor.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_name =  'storage_users';")
        print(check_sql)
        if (check_sql is None) or (len(check_sql) == 7):
            cursor.execute("CREATE TABLE storage_users("
                       "increment BIGINT PRIMARY KEY, "
                       "user_id BIGINT, user_login TEXT, user_name TEXT, is_prime BOOL, "
                       "balance DECIMAL, all_refill INTEGER, reg_date TIMESTAMP)")
            logging.info("cursor was not found(1/8) | Creating...")
        else:
            check_create_users = [c for c in check_sql]
            logging.info("cursor was found(1/8)")

        # Создание БД с хранением данных платежных систем
        check_sql = cursor.execute("PRAGMA table_info(storage_payment)")
        check_sql = check_sql.fetchall()
        check_create_payment = [c for c in check_sql]
        if len(check_create_payment) == 6:
            logging.info("cursor was found(2/8)")
        else:
            cursor.execute("CREATE TABLE storage_payment("
                    "qiwi_login TEXT, qiwi_token TEXT, "
                    "qiwi_private_key TEXT, qiwi_nickname TEXT, "
                    "way_payment TEXT, status TEXT)")
            
            cursor.execute("INSERT INTO storage_payment("
                    "qiwi_login, qiwi_token, "
                    "qiwi_private_key, qiwi_nickname, "
                    "way_payment, status) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    ["None", "None", "None", "None", "form", "False"])
            logging.info("cursor was not found(2/8) | Creating...")
        
        check_sql = cursor.execute("PRAGMA table_info(storage_crypto_payment)")
        check_sql = check_sql.fetchall()
        check_create_payment = [c for c in check_sql]
        if len(check_create_payment) == 7:
            logging.info("cursor was found(3/10)")
        else:
            cursor.execute("CREATE TABLE storage_crypto_payment("
                       "address TEXT, user_id INTEGER,"
                       "user_login TEXT, status bool, "
                       "currency TEXT, except_value Decimal, unix_time INTEGER)")
            logging.info("cursor was not found(3/10) | Creating...")
    

        # Создание БД с хранением настроек
        check_sql = cursor.execute("PRAGMA table_info(storage_settings)")
        check_sql = check_sql.fetchall()
        check_create_settings = [c for c in check_sql]
        if len(check_create_settings) == 6:
            logging.info("cursor was found(4/10)")
        else:
            cursor.execute("CREATE TABLE storage_settings("
                       "contact INTEGER, faq TEXT, "
                       "status TEXT, status_buy TEXT,"
                       "profit_buy TEXT, profit_refill TEXT)")
            sql = "INSERT INTO storage_settings(" \
                  "contact, faq, status, status_buy, profit_buy, profit_refill) " \
                  "VALUES (?, ?, ?, ?, ?, ?)"
            now_unix = int(time.time())
            parameters = ("ℹ Контакты. Измените их в настройках бота.\n"
                          "➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                          f"{bot_description}",
                          "ℹ Информация. Измените её в настройках бота.\n"
                          "➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                          f"{bot_description}",
                          "True", "True", now_unix, now_unix)
            cursor.execute(sql, parameters)
            logging.info("cursor was not found(4/10) | Creating...")

        # Создание БД с хранением пополнений пользователей
        check_sql = cursor.execute("PRAGMA table_info(storage_refill)")
        check_sql = check_sql.fetchall()
        check_create_refill = [c for c in check_sql]
        if len(check_create_refill) == 10:
            logging.info("cursor was found(5/10)")
        else:
            cursor.execute("CREATE TABLE storage_refill("
                       "increment INTEGER SERIAL PRIMARY KEY,"
                       "user_id INTEGER, user_login TEXT, "
                       "user_name TEXT, comment TEXT, "
                       "amount TEXT, receipt TEXT, "
                       "way_pay TEXT, dates TIMESTAMP, "
                       "dates_unix TEXT)")
            logging.info("cursor was not found(5/10) | Creating...")

        # Создание БД с хранением категорий
        check_sql = cursor.execute("PRAGMA table_info(storage_category)")
        check_sql = check_sql.fetchall()
        check_create_category = [c for c in check_sql]
        if len(check_create_category) == 3:
            logging.info("cursor was found(6/10)")
        else:
            cursor.execute("CREATE TABLE storage_category("
                       "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "category_id INTEGER, category_name TEXT)")
            logging.info("cursor was not found(6/10) | Creating...")

        # Создание БД с хранением позиций
        check_sql = cursor.execute("PRAGMA table_info(storage_position)")
        check_sql = check_sql.fetchall()
        check_create_position = [c for c in check_sql]
        if len(check_create_position) == 14:
            logging.info("cursor was found(7/10)")
        else:
            cursor.execute("CREATE TABLE storage_position("
                       "increment SERIAL INTEGER PRIMARY KEY,"
                       "position_id INTEGER, position_name TEXT, position_type INTEGER,"
                       "position_price INTEGER, position_price_day INTEGER, position_price_week INTEGER, position_price_mounth INTEGER, position_discription TEXT,"
                       "position_image TEXT, position_date TIMESTAMP, "
                       "category_id INTEGER, base_path TEXT, path_change TEXT)")
            logging.info("cursor was not found(7/10) | Creating storage_position...")
        # Создание БД с хранением товаров
        check_sql = cursor.execute("PRAGMA table_info(storage_item)")
        check_sql = check_sql.fetchall()
        check_create_item = [c for c in check_sql]
        if len(check_create_item) == 9:
            logging.info("cursor was found(8/10)")
        else:
            cursor.execute("CREATE TABLE storage_item("
                       "increment SERIAL INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "item_id INTEGER, item_data TEXT, position_type INTEGER,"
                       "position_id INTEGER, category_id INTEGER, "
                       "creator_id INTEGER, creator_name TEXT, "
                       "add_date TIMESTAMP)")
            logging.info("cursor was not found(8/10) | Item Selling table Creating...")

        check_sql = cursor.execute("PRAGMA table_info(licence_purhases)")
        check_sql = check_sql.fetchall()
        check_create_item = [c for c in check_sql]
        if len(check_create_item) == 18:
            logging.info("cursor was found(9/10)")
        else:
            cursor.execute("CREATE TABLE licence_purhases("
                        "increment SERIAL INTEGER PRIMARY KEY,"
                        "HWID TEXT, licence_time Timestamp, change_times INTEGER,"
                        "user_id INTEGER, user_login TEXT, "
                        "user_name TEXT, receipt TEXT, "
                        "item_count INTEGER, item_price TEXT, "
                        "item_price_one_item TEXT, item_position_id INTEGER, "
                        "item_position_name TEXT, item_buy TEXT, "
                        "balance_before TEXT, balance_after TEXT, "
                        "buy_date TIMESTAMP, buy_date_unix TEXT)")
            logging.info("cursor was not found(9/10) | Licence Table Creating...")
        
        

        # Создание БД с хранением покупок
        check_sql = cursor.execute("ALL_TAB_COLUMNS table_info(storage_purchases)")
        check_sql = check_sql.fetchall()
        check_create_purchases = [c for c in check_sql]
        if len(check_create_purchases) == 15:
            logging.info("cursor was found(10/10)")
        else:
            cursor.execute("CREATE TABLE storage_purchases("
                       "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "user_id INTEGER, user_login TEXT, "
                       "user_name TEXT, receipt TEXT, "
                       "item_count INTEGER, item_price TEXT, "
                       "item_price_one_item TEXT, item_position_id INTEGER, "
                       "item_position_name TEXT, item_buy TEXT, "
                       "balance_before TEXT, balance_after TEXT, "
                       "buy_date TIMESTAMP, buy_date_unix TEXT)")
            logging.info("cursor was not found(10/10) | Creating...")

        cursor.commit()
