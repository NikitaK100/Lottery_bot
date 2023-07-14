from aiogram import types
from aiogram.dispatcher.filters import CommandStart

import MESSAGE
from keyboard.inline.info_keyboard import keyboard_information
from keyboard.inline.keyboard_account import keyboard_add_money
from keyboard.inline.start_keyboard import keyboard_authorization
from loader import dp
from utils.db_api.schemas import quick_commands as db2

# Меню регистрации и входа в свой аккаунт 

@dp.message_handler(CommandStart())
async def start(message: types.Message):
    await message.answer(MESSAGE.all_messages['start'], reply_markup=keyboard_authorization)


@dp.callback_query_handler(text='registration')
async def registration_keyboard(call: types.CallbackQuery):
    user_id = call.from_user.id
    name = call.from_user.full_name
    if not await db2.select_user(id=user_id):
        await db2.add_user(id=user_id, name=name)
        await call.message.edit_text('Регистрация прошла успешно!\n'
                                     'Осталось только войти',
                                     reply_markup=keyboard_authorization)
    else:
        await db2.select_user(id=user_id)
        await call.message.edit_text(text='Вы уже регистрировались ранее\n'
                                          'Осталось только войти',
                                     reply_markup=keyboard_authorization)
    await call.answer()


@dp.callback_query_handler(text='entrance')
async def entrance_keyboard(call: types.CallbackQuery):
    user_id = call.from_user.id
    name = call.from_user.full_name
    wallet = await db2.select_user(id=user_id)
    if await db2.select_user(id=user_id):
        await call.message.edit_text(f'Добро пожаловать <b>{name}</b>\n\n'
                                     f'Баланс: <b>{wallet.wallet}</b> монет \n\n'
                                     f'🔻Выберите, что хотите сделать🔻',
                                     reply_markup=keyboard_add_money)
    elif not await db2.select_user(id=user_id):
        await call.message.edit_text('Вы ещё не зарегистрированы',
                                     reply_markup=keyboard_authorization)
    await call.answer()


@dp.callback_query_handler(text='information')
async def information_keyboard(call: types.CallbackQuery):
    # Длинный сообщения находятся в отдельной папке MESSAGE.py в виде словаря
    await call.message.edit_text(MESSAGE.all_messages['info'], reply_markup=keyboard_information)
    await call.answer()


@dp.callback_query_handler(text='back')
async def answer_back(call: types.CallbackQuery):
    await call.message.edit_text(MESSAGE.all_messages['start'],
                                 reply_markup=keyboard_authorization)
    await call.answer()
