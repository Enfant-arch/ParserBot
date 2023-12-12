# - *- coding: utf- 8 - *-
from utils.db_api.psql  import get_userx, get_purchasesx


def get_user_profile(user_id):
    get_user = get_userx(user_id=user_id)
    count_items = 0
    msg = f"<b>👤 Ваш профиль:</b>\n" \
          f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
          f"🔑 Мой ID: <code>{get_user[1]}</code>\n" \
          f"📇 Логин: <b>@{get_user[2]}</b>\n" \
          f"📅 Регистрация: <code>{get_user[6]}</code>\n" \
          f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" 
    
    return msg


def search_user_profile(user_id):
    get_status_user = get_userx(user_id=user_id)
    count_items = 0
    msg = f"<b>📱 Профиль пользователя:</b> <a href='tg://user?id={get_status_user[1]}'>{get_status_user[3]}</a>\n" \
          f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
          f"🔑 ID: <code>{get_status_user[1]}</code>\n" \
          f"👤 Логин: <b>@{get_status_user[2]}</b>\n" \
          f"Ⓜ Имя: <a href='tg://user?id={get_status_user[1]}'>{get_status_user[3]}</a>\n" 
    
    return msg
