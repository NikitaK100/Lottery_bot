
from aiogram.dispatcher.filters.state import StatesGroup, State



class GetCoin(StatesGroup):
    get_coin = State()
    confirm = State()

