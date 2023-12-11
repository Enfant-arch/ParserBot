from aiogram.dispatcher.filters.state import State, StatesGroup

class Payment(StatesGroup):
    money = State()

class PaymentCredit(StatesGroup):
    money = State()