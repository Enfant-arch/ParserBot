from aiogram.dispatcher.filters.state import State, StatesGroup

class Broadcast(StatesGroup):
    text = State()
    photo = State()
    link = State()
    time = State()
    accept = State()

class Un_bunUser(StatesGroup):
    ids = State()
    accept = State()

class bunUser(StatesGroup):
    ids = State()
    accept = State()

class promoAdd(StatesGroup):
    text = State()
    money = State()
    accept = State()
    
class ChangePrice(StatesGroup):
    name = State()
    new_price = State()
    accept = State()