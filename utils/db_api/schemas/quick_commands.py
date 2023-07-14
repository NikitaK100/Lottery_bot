from utils.db_api.schemas.user import User


async def add_user(id: int, name: str, wallet: int = 0):
    try:
        user = User(id=id, name=name, wallet=wallet)
        await user.create()
    except Exception as err:
        print(f'Exception from User TABLE:'
              f'{err}')


async def select_all_users():
    users = await User.query.gino.all()
    return users


async def select_user(id: int):
    user = await User.query.where(User.id == id).gino.first()
    return user


async def count_users():
    total = await User.db.func.count(User.id).gino.scalar()
    return total


async def update_wallet(id, wallet):
    user = await User.get(id)
    await user.update(id=id, wallet=wallet).apply()




