import logging

from aiogram import Dispatcher, Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data import config
from utils.db_api.schemas import quick_commands as db

bot = Bot(token=config.API_TOKEN, parse_mode=types.ParseMode.HTML)

storage = MemoryStorage()

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)
logging.basicConfig(level=logging.INFO)

dp = Dispatcher(bot, storage=storage)

__all__ = ['bot', 'storage', 'dp', 'db']
