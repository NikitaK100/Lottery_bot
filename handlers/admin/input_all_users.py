from attr import dataclass
from data.config import admin_id
from aiogram import types
from utils.db_api.schemas import lottery_participants as db4
from utils.db_api.schemas import commands_lottery as db3
from data.config import admins
from loader import dp
from states.input_quantity_users import InputUsers
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from keyboard.inline.admin_keyboard.admin_back_btn import keyboard_admin_back
from keyboard.inline.admin_keyboard.admin_keyboard import keyboard_admin


data_callback = CallbackData('lottery', 'key', 'lottery_id')


async def get_keyboard_lottery_id(key='lottery_id', lottery_id: str='0'):

    list_participants_all_lotterys = [{'id': list_participants.id, 
                                       'name': list_participants.name} for  list_participants 
                                       in await db3.select_all()]

    markup = InlineKeyboardMarkup(row_width=1)
    for number_lottery in list_participants_all_lotterys:
        lottery_id = number_lottery
        markup.insert(
            InlineKeyboardButton(
                text=number_lottery['name'],
                callback_data=data_callback.new(key=key, lottery_id=lottery_id['id'])
            )
        )
    markup.insert(
            InlineKeyboardButton(
                text='Назад',
                callback_data='admin_back')
            )
    
    return markup


@dp.callback_query_handler(user_id=admins, text='list_everething_participants')
async def select_lottery(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text("Выбирите лотерею:", reply_markup=await get_keyboard_lottery_id())


@dp.callback_query_handler(data_callback.filter(key='lottery_id'))
async def my_callback_foo(call: types.CallbackQuery, callback_data: dict):

    await call.answer()

    lottery_id=int(callback_data.get('lottery_id'))

    list_participants = [{'name': participants.name,
                          'id': participants.id} for participants 
                          in await db4.select_all_lottery_users(lottery_id=lottery_id)]
    

    await call.message.edit_text('\n\n'.join([ participants["name"] + ':' + str(participants["id"]) for participants in list_participants]),
                                reply_markup=keyboard_admin_back)


@dp.callback_query_handler(text='admin_back')
async def admin_back_btn(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text(f'🙋Здравствуйте <b>{call.message.from_user.full_name}</b>\n\n'
                              f'Вы находитесь в панеле администратора\n'
                              'Выбирете, одно из действий:',
                              reply_markup=keyboard_admin)
