from aiogram import Dispatcher
from gino import Gino

from data import config

db = Gino()


async def on_startup(dispatcher: Dispatcher):
    print('Установка связи с PostgreSQL')
    await db.set_bind(config.postgres_uri)  # теперь мы установили связь с db
