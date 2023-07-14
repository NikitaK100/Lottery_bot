from utils.db_api.db_gino import db
from utils.db_api.schemas.user import PurchaseLottery


async def add_user(id: int, lottery_id: int, name: str):
    try:
        user = PurchaseLottery(id=id, lottery_id=lottery_id, name=name)
        await user.create()
    except Exception as err:
        print(f'Exception from PurchaseLottery TABLE:\n'
              f'{err}')


async def count_users(lottery_id: int):
    total = await db.select([db.func.count()]).where(PurchaseLottery.lottery_id == lottery_id).gino.scalar()
    return total


async def select_user(id: int):
    user = await PurchaseLottery.query.where(PurchaseLottery.id == id).gino.first()
    return user


async def select_all():
    lotterys = await PurchaseLottery.query.gino.all()
    return lotterys 


async def select_all_lottery_where_id(id: int):
    lottery = await PurchaseLottery.query.where(PurchaseLottery.id == id).gino.all()
    return lottery


async def select_all_lottery_users(lottery_id: int):
    users = await PurchaseLottery.query.where(PurchaseLottery.lottery_id == lottery_id).gino.all()
    return users


async def select_id_lottery(lottery_id: int):
    user = await PurchaseLottery.query.where(PurchaseLottery.lottery_id == lottery_id).gino.first()
    return user

