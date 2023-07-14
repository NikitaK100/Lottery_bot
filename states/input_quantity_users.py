from aiogram.dispatcher.filters.state import StatesGroup, State


class InputUsers(StatesGroup):
    get_number_lottery = State()
    input_users = State()
