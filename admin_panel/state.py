from aiogram.dispatcher.filters.state import State, StatesGroup

class Admin(StatesGroup):
    add = State()
    delete = State()

class Channel(StatesGroup):
    add = State()
    delete = State()

class Sending(StatesGroup):
    start = State()

class BlackList(StatesGroup):
    ban = State()
    unban = State()

class AddButton(StatesGroup):
    text = State()
    url = State()

class Support(StatesGroup):
    send_to = State()
    send_from = State()
    get_aim = State()
    send_message = State()

class Agreement(StatesGroup):
    edit = State()