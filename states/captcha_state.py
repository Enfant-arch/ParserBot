from aiogram.dispatcher.filters.state import State, StatesGroup

class CAPTCHA(StatesGroup):
    correct = State()
    check = State()