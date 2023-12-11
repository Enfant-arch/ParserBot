# - *- coding: utf- 8 - *-
from aiogram.dispatcher.filters.state import State, StatesGroup


class StorageCategory(StatesGroup):
    here_change_category_name = State()
    here_input_category_name = State()

    here_cache_category_id = State()
    here_cache_category_remover = State()

class StoragePosition(StatesGroup):
    here_input_position_discription = State()
    here_input_type_position = State()
    here_input_position_price = State()

    here_input_position_price_per_day = State()
    here_input_position_price_per_week = State()
    here_input_position_price_per_month = State()

    here_input_position_image = State()
    here_input_position_name = State()
    here_input_position_basepath = State()
    here_input_position_changepath = State()
    here_change_position_discription = State()
    here_change_position_price = State()
    here_change_position_image = State()
    here_change_position_name = State()

    here_cache_category_id = State()
    here_cache_position_id = State()
    here_cache_position_remover = State()

class StorageItems(StatesGroup):
    here_cache_add_item_position_id = State()
    here_cache_add_item_category_id = State()
    here_cache_add_item_remover = State()
    here_count_add_items = State()

    here_del_items = State()
    here_add_items = State()
