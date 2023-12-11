from aiogram.types import InlineKeyboardMarkup, InlineQuery
from aiogram.types import InlineKeyboardButton



by_name = InlineKeyboardButton("🔍 По названию", callback_data='by:query')
by_catalog = InlineKeyboardButton("🗂 По категории", callback_data='by:category')
megaCashe= InlineKeyboardButton("💸 МЕГА-КЕШБЕК", callback_data="by:cachback")
toHome = InlineKeyboardButton("⬅ На главную", callback_data="Home")
parsing_InlineBoard = InlineKeyboardMarkup(row_width=1).add(by_name, by_catalog, megaCashe, toHome)

back = InlineKeyboardButton("⬅ Назад", callback_data="parser:back")
select_parsing_Inline = InlineKeyboardMarkup(row_width=1).add(back)