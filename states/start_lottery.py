from aiogram.dispatcher.filters.state import StatesGroup, State


class StartLottery(StatesGroup):
    get_number_lottery = State()
    select_winner = State()