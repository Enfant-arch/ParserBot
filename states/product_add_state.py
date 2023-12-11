from aiogram.dispatcher.filters.state import State, StatesGroup

class ProductAdd(StatesGroup):
    name = State()
    add = State()
    accept = State()

class ProductBuy(StatesGroup):
    product = State()
    accept = State()