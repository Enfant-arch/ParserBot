from aiogram.dispatcher.filters.state import State, StatesGroup

class Parser(StatesGroup):
    input = State()
