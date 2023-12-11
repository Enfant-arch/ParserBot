from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from admin_panel.panel import core


def menu():
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("📢 Каналы", callback_data="menu_channels"),
        InlineKeyboardButton("👤 Админы", callback_data="menu_admins"),
        InlineKeyboardButton("📨 Рассылка", callback_data="menu_sending"),
        InlineKeyboardButton("🈲 Чёрный список", callback_data="menu_black_list"),
        InlineKeyboardButton("👨🏼‍💻 Тех. поддержка", callback_data="menu_support"),
        InlineKeyboardButton("🗃 Архив бота", callback_data="menu_history"),
        InlineKeyboardButton("📜 Соглашение", callback_data="menu_agreement"))


def menu_admins(admins):
    k = InlineKeyboardMarkup(row_width=3)
    for i in admins:
        if i[0] != core.main_admin:
            if i[1] == "locked":
                k.add(
                    InlineKeyboardButton(f"id{i[0]}", callback_data="none"),
                    InlineKeyboardButton("🗑", callback_data="admin_locked"),
                    InlineKeyboardButton("🔒", callback_data=f"unlock_delete_admin_{i[0]}"))
            elif i[1] == "unlocked":
                k.add(
                    InlineKeyboardButton(f"id{i[0]}", callback_data="none"),
                    InlineKeyboardButton("🗑", callback_data=f"delete_admin_{i[0]}"),
                    InlineKeyboardButton("🔓", callback_data=f"refresh_admin"))
    for i in range(0, 5 - round(len(admins))):
        k.add(
            InlineKeyboardButton("➕", callback_data="add_admin")
        )
    k.add(InlineKeyboardButton("← Назад", callback_data="to_menu"),
          InlineKeyboardButton("♻", callback_data="refresh_admin"))
    return k


def menu_channels(channels):
    k = InlineKeyboardMarkup(row_width=3)
    for i in channels:
        if i[1] == "locked":
            k.add(
                InlineKeyboardButton(f"{i[0]}", callback_data="none"),
                InlineKeyboardButton("🗑", callback_data="channel_locked"),
                InlineKeyboardButton("🔒", callback_data=f"unlock_delete_channel_{i[0]}"))
        elif i[1] == "unlocked":
            k.add(
                InlineKeyboardButton(f"{i[0]}", callback_data="none"),
                InlineKeyboardButton("🗑", callback_data=f"delete_channel_{i[0]}"),
                InlineKeyboardButton("🔓", callback_data=f"refresh_channel"))
    for i in range(0, 5 - round(len(channels))):
        k.add(InlineKeyboardButton("➕", callback_data="add_channel"))
    k.add(InlineKeyboardButton("← Назад", callback_data="to_menu"),
          InlineKeyboardButton("♻", callback_data="refresh_channel"))
    return k


def menu_sending():
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("📨 Начать рассылку", callback_data="start_sending"),
        InlineKeyboardButton("➕ Кнопка", callback_data="add_button"),
        InlineKeyboardButton("← Назад", callback_data="to_menu"))


def accept_sending():
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("✅ Подтвердить рассылку", callback_data="accept_start_sending"),
        InlineKeyboardButton("✖", callback_data="close"))


def accept_button():
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("✅ Добавить в новый ряд", callback_data="accept_add_button_1"),
        InlineKeyboardButton("✅ Добавить в последний ряд", callback_data="accept_add_button_2"),
        InlineKeyboardButton("✖ Закрыть", callback_data="close")
    )


def new_buttons(old: InlineKeyboardMarkup, new: list, insert: bool):
    k = InlineKeyboardMarkup(row_width=5)
    new = InlineKeyboardButton(new[0], new[1])
    if old:
        for row in old.inline_keyboard:
            for i in range(len(row)):
                if i == 0:
                    k.add(row[i])
                else:
                    k.insert(row[i])
        if insert:
            k.insert(new)
        else:
            k.add(new)
    else:
        k.add(new)
    return k


def subscribe_channels(channels):
    k = InlineKeyboardMarkup(row_width=1)
    for i in range(len(channels)):
        k.add(InlineKeyboardButton(f"◾ Канал #{i + 1}", channels[i][1]))
    k.add(InlineKeyboardButton("✅ Подтвердить", callback_data="accept_subscription"))
    return k


def menu_black_list():
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("🥶 Забанить", callback_data="ban_user"),
        InlineKeyboardButton("🥰 Разбанить", callback_data="unban_user"),
        InlineKeyboardButton("← Назад", callback_data="to_menu"))


def ban_during():
    return InlineKeyboardMarkup(row_width=3).add(
        InlineKeyboardButton("➕ 1h", callback_data="add_1h"),
        InlineKeyboardButton("➕ 4h", callback_data="add_4h"),
        InlineKeyboardButton("➕ 12h", callback_data="add_12h")).add(
        InlineKeyboardButton("♾", callback_data="set_999999h"),
        InlineKeyboardButton("0️⃣", callback_data="set_0h")).add(
        InlineKeyboardButton("➖ 1h", callback_data="minus_1h"),
        InlineKeyboardButton("➖ 4h", callback_data="minus_4h"),
        InlineKeyboardButton("➖ 12h", callback_data="minus_12h"),
        InlineKeyboardButton("✅ Подтвердить бан", callback_data="accept_ban")).add(
        InlineKeyboardButton("✖", callback_data="close")
    )


def menu_history():
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("📊 Общая статистика", callback_data="menu_history_general"),
        InlineKeyboardButton("➕ Приход", callback_data="menu_history_income"),
        InlineKeyboardButton("👥 Пользователи", callback_data="menu_history_users"),
        InlineKeyboardButton("📫 Рассылки", callback_data="menu_history_sendings"),
        InlineKeyboardButton("📑 Лог текущей сессии", callback_data="menu_history_log")).add(
        InlineKeyboardButton("← Назад", callback_data="to_menu"))


def menu_support(unread_messages: int, locked=True):
    k = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton(f"📫 Сообщения [{unread_messages}]", callback_data="get_support_messages"))
    k.add(InlineKeyboardButton("📨 Отправить сообщение от тех. поддержки", callback_data="send_message_from_support"))
    if locked:
        k.add(
            InlineKeyboardButton("🗑", callback_data="locked"),
            InlineKeyboardButton("🔒", callback_data="unlock_support_messages"))
    else:
        k.add(
            InlineKeyboardButton("🗑", callback_data="clean_menu_support"),
            InlineKeyboardButton("🔓", callback_data="lock_support_messages"))
    k.add(InlineKeyboardButton("♻", callback_data="refresh_support_messages"))
    k.add(InlineKeyboardButton("← Назад", callback_data="to_menu"))
    return k


def message_menu(message_id, user_id):
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("✅ Прочитано", callback_data=f"delete_support_message_{message_id}"),
        InlineKeyboardButton("🗣 Ответить", callback_data=f"answer_support_message_{user_id}"))


def support_messages(messages):
    k = InlineKeyboardMarkup(row_width=1)
    for message in messages:
        k.add(InlineKeyboardButton(f"{message[3][:20]}...", callback_data=f"open_support_message_{message[4]}"))
    if len(k.inline_keyboard) == 0:
        k.add(InlineKeyboardButton("◾ Здесь пусто!", callback_data="locked"))
    k.add(InlineKeyboardButton("← Назад", callback_data="menu_support"))
    return k


def menu_agreement():
    k = InlineKeyboardMarkup(row_width=2)

    k.add(
        InlineKeyboardButton("👁 Показать", callback_data="show_agreement"),
        InlineKeyboardButton("✏ Изменить", callback_data="edit_agreement"))
    if bool(core.agreement):
        k.add(InlineKeyboardButton("🎾 Выключить", callback_data="turn_off_agreement"))
    else:
        k.add(InlineKeyboardButton("⚾ Включить", callback_data="turn_on_agreement"))
    k.add(InlineKeyboardButton("← Назад", callback_data="to_menu"))
    return k


def accept_agreement():
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("✅ Принять", callback_data="accept_agreement"))


def close():
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("✖", callback_data="close"))