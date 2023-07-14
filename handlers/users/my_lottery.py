from loader import dp 
from aiogram import types 
from utils.db_api.schemas import lottery_participants
from utils.db_api.schemas import commands_lottery
from keyboard.inline.keyboard_back_account import keyboard_back

@dp.callback_query_handler(text='my_lottery')
async def my_lottery_list(call: types.CallbackQuery):
    """
    Функция выводит список лотерей в которых участвует юзер
    """
    user_id = call.from_user.id
    list_activ_lottery = await lottery_participants.select_all_lottery_where_id(id=user_id)
    list_my_lottery_id = [await commands_lottery.select_id_lottery(lottery.lottery_id) for lottery in list_activ_lottery]
    list_card_lottery = []
    for card_lottery in list_my_lottery_id:
        list_card_lottery.append(card_lottery.lottery_id)
    await call.message.edit_text(f'\n\n---------------------------------------------------------\n\n'.join(list_card_lottery), 
                                reply_markup=keyboard_back)

    



