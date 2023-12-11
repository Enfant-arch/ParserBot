# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Кнопки при поиске профиля через админ-меню
open_profile_inl = InlineKeyboardMarkup()
input_kb = InlineKeyboardButton(text="💵 Пополнить", callback_data="user_input")
mybuy_kb = InlineKeyboardButton(text="🎁 Мои покупки", callback_data="my_buy")
myLicence_kb = InlineKeyboardButton(text="🌩 Мои Лицензии", callback_data="my_licence")
open_profile_inl.add(input_kb, mybuy_kb)
open_profile_inl.add(myLicence_kb)


chages_licence = InlineKeyboardMarkup()
change = InlineKeyboardButton(text="Изенить HWID", callback_data="change_hwid")
back_profle = InlineKeyboardButton(text="◀️Назад", callback_data="back_profile")
chages_licence.add(change)
chages_licence.add(back_profle)

# Кнопка с возвратом к профилю
to_profile_inl = InlineKeyboardMarkup()
to_profile_inl.add(InlineKeyboardButton(text="🪪 Профиль", callback_data="user_profile"))


confirmation = InlineKeyboardMarkup()
accepting = InlineKeyboardButton(text="✅Подтвердить", callback_data="confirm")
cancel_accepting = InlineKeyboardButton(text="❌Отмена", callback_data="cancel")
confirmation.add(accepting)
confirmation.add(cancel_accepting)