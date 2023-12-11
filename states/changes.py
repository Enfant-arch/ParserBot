from aiogram.dispatcher.filters.state import State, StatesGroup

class ChangeAD(StatesGroup):
    position = State()
    BtnText = State()
    Reply = State()
    accept = State()

class ChangeLink(StatesGroup):
    link = State()
    accept = State()