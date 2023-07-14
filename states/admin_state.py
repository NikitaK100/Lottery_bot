from aiogram.dispatcher.filters.state import StatesGroup, State


class Admin(StatesGroup):
    id = State()
    name = State()
    description = State()
    photo = State()
    quantity = State()
    price = State()
    confirm = State()

