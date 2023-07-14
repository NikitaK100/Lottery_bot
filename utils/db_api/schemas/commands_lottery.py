from utils.db_api.schemas.user import Participants
from utils.db_api.db_gino import db 


async def add_user(id: int, id_admin: int, name: str, description: str, photo: str, price: int, quantity: int, index_id: int = None):
    try:
        user = Participants(id=id, index_id=index_id, id_admin=id_admin, name=name, description=description, photo=photo,
                            price=price, quantity=quantity)
        await user.create()
    except Exception as err:
        print(f'Exception from Participants TABLE:'
              f'{err}')


async def select_user(id_admin: int):
    user = await Participants.query.where(Participants.id_admin == id_admin).gino.first()
    return user


async def select_id():
    users = await Participants.query.gino.all()
    return users


async def select_id_lottery(id: int):
    user = await Participants.query.where(Participants.id == id).gino.first()
    return user



async def select_all():
    lotterys = await Participants.query.gino.all()
    return lotterys


async def select_all_id_lottery(id: int):
    user = await Participants.query.where(Participants.id == id).gino.all()
    return user


async def count_lottery():
    lotterys = await db.func.count(Participants.id).gino.scalar()
    return lotterys


async def delete_lottery(id: int):
    items = await Participants.delete.where(Participants.id == id).gino.first()
    return items
