from utils.db_api import db_gino
from utils.db_api.db_gino import db


async def on_startup(dp):
    print('Подключаем БД')
    await db_gino.on_startup(dp)
    print('Готово')
    # print("Чистим базу")
    # await db.gino.drop_all()
    # print("Готово")
    print("Создаём таблицы")
    await db.gino.create_all()
    print("Готово")
    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
