from aiogram import types
from keyboard.inline.keyboard_back_account import keyboard_back
from keyboard.inline.keyboards_mixin import confirm_keyboards
from loader import dp, bot 
from aiogram.dispatcher.storage import FSMContext
from utils.db_api.schemas import quick_commands as db2
from utils.db_api.schemas import commands_lottery as db3
from utils.db_api.schemas import lottery_participants as db4
from keyboard.inline.keyboard_account import keyboard_add_money
from utils.db_api.schemas.user import Participants

# Интерфейс покупки лоттерей и обработки исключений связанный с покупкой


@dp.callback_query_handler(text='buy', state='buying_lottery')
async def buy_lottery(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    user_id = call.from_user.id
    data = await state.get_data()
    number_lottery = data.get('lottery_id')
    data_db2 = await db2.select_user(id=user_id)
    data_db_3 = await db3.select_id_lottery(id=number_lottery)
    data_db4 = await db4.select_user(id=user_id)
    count = await db4.count_users(lottery_id=number_lottery)

    if data_db2.wallet < data_db_3.price:
        await call.message.edit_text('У вас недостаточно монет',
                                  reply_markup=keyboard_back)
        await state.reset_state() 

    elif await db4.count_users(lottery_id=number_lottery) == data_db_3.quantity:
        await call.message.edit_text(f'Набрано маскимальное кол-во участников {count}',
                                  reply_markup=keyboard_back)
        await state.reset_state()

    elif data_db2.wallet >= data_db_3.price:
        # Проверка на попытку второй раз купить одну и ту же лотерею 
        if data_db4:                                                                        # если id юзера уже есть в базе
            list_db4 = [str(participant.id) + str(participant.lottery_id)                   # достал все id и lottery_id + сконкотенировал
                        for participant in await db4.select_all_lottery_where_id(user_id)]  
            list_db4.append(str(user_id) + str(number_lottery))                             # добавил в список значения которые хочет передать юзер
            filtering_list_db4 = set(list_db4)                                              # set оставляет только уникальные значения

            if len(filtering_list_db4) < len(list_db4):                             # если отфильтрованный список < не отфильтрованного
                await call.message.edit_text('Вы уже учасвствуйте в этой лотерее!', # тогда запрещаем покупать лотерею 
                                        reply_markup=keyboard_back)
                await state.reset_state()

            else:
                wallet_balance = await db2.select_user(id=call.from_user.id)
                buy = wallet_balance.wallet - data_db_3.price
                await db2.update_wallet(id=call.from_user.id, wallet=buy)
                await db4.add_user(id=call.from_user.id,
                                lottery_id=number_lottery,
                                name=call.from_user.full_name)
                await call.message.edit_text('Покупка прошла успешно!',
                                            reply_markup=keyboard_back)
                await state.finish()
            
        else:
            wallet_balance = await db2.select_user(id=call.from_user.id)
            buy = wallet_balance.wallet - data_db_3.price
            await db2.update_wallet(id=call.from_user.id, wallet=buy)   #  списываем монеты из личного кабинета 
            await db4.add_user(id=call.from_user.id,                    # покупка прошла успешно добавляем данные в бд
                            lottery_id=number_lottery,
                            name=call.from_user.full_name)
            await call.message.edit_text('Покупка прошла успешно!',
                                        reply_markup=keyboard_back)
            await state.finish()


@dp.callback_query_handler(text='cancel_buy', state='buying_lottery')
async def cancel_buy_lottery(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    user_id = call.from_user.id
    name = call.from_user.full_name
    wallet = await db2.select_user(id=user_id)
    await call.message.edit_text(f'Добро пожаловать <b>{name}</b>\n\n'
                                f'Баланс: <b>{wallet.wallet}</b> монет \n\n'
                                f'🔻Выберите, что хотите сделать🔻',
                                reply_markup=keyboard_add_money)
    await state.reset_state()



