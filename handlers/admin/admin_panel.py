import random
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from sqlalchemy import desc

from data.config import admins
from keyboard.inline.admin_keyboard.admin_keyboard import keyboard_admin
from keyboard.inline.keyboard_confirm import confirmation_keyboard
from loader import dp, bot
from states.admin_state import Admin
from utils.db_api.schemas import commands_lottery as db3


@dp.message_handler(user_id=admins, commands=['admin'])
async def start_admin_panel(message: types.Message):
    await message.answer(f'🙋Здравствуйте <b>{message.from_user.full_name}</b>\n\n'
                         f'Вы находитесь в панеле администратора\n'
                         'Выбирете, одно из действий:',
                         reply_markup=keyboard_admin)


@dp.message_handler(user_id=admins, commands='cancel', state=Admin)
async def cancel(message: types.Message, state: FSMContext):
    await message.answer('Вы отменили создание лотереи',
                            reply_markup=keyboard_admin)
    await state.reset_state()


@dp.callback_query_handler(user_id=admins, text='create_lottery')
async def state_id(call: types.CallbackQuery, state: FSMContext):
    id_lot = random.randint(1000, 10000)
    if await db3.select_id_lottery(id=id_lot):
        await call.message.answer('Такая лотерея уже существует!',
                             reply_markup=keyboard_admin)
        await state.reset_state()
    else:
        await state.update_data(
            {
                'id_lottery': id_lot
            }
        )
        await call.message.answer(f'id лотереи: {id_lot}\n'
                             f'Укажите имя лотереи:\n\n'
                             f'Что бы выйти из конструктора: /cancel')
        await Admin.name.set()


@dp.message_handler(user_id=admins, state=Admin.name)
async def get_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(
        {
            'name': name
        }
    )
    await message.answer(f'Имя: <b>{name}</b>\n'
                         f'Пришлите мне описание лотереи: \n\n'
                         f'Что бы выйти из конструктора: /cancel')
    await Admin.description.set()




@dp.message_handler(user_id=admins, state=Admin.description)
async def state_name(message: types.Message, state: FSMContext):
    description = message.text
    await state.update_data(
        {
            'description': description
        }
    )

    await message.answer(f'Текст: {description}\n'
                         f'Пришлите мне фото к посту(не документ)\n\n'
                         f'Что бы выйти из конструктора: /cancel')
    await Admin.photo.set()


@dp.message_handler(user_id=admins, state=Admin.photo, content_types=types.ContentTypes.PHOTO)
async def add_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(
        {
            'photo_lottery': photo
        }
    )
    await message.answer('Введите желаемое кол-во участников: ')
    await Admin.quantity.set()


@dp.message_handler(user_id=admins, state=Admin.quantity)
async def add_quantity(message: types.Message, state: FSMContext):
    quantity = int(message.text)
    await state.update_data(
        {
            'quantity': quantity
        }
    )
    await message.answer('Сколько будет стоить один билет?')
    await Admin.price.set()


@dp.message_handler(user_id=admins, state=Admin.price)
async def add_quantity(message: types.Message, state: FSMContext):
    price = int(message.text)
    await state.update_data(
        {
            'price': price
        }
    )
    data = await state.get_data()
    id = data.get('id_lottery')
    name = data.get('name')
    description = data.get('description')
    photo = data.get('photo_lottery')
    quantity = data.get('quantity')
    price = data.get('price')
    await message.answer_photo(photo=photo,
                               caption='Выглядит следующим образом:\n\n'
                                       f'Лотерея №{id}\n\n'
                                       f'<b>{name}</b>\n\n'
                                       f'{description}\n\n'
                                       f'Максимальное кол-во участников:{quantity}\n\n'
                                       f'Цена за билет: {price}',
                               reply_markup=confirmation_keyboard
                               )
    await Admin.confirm.set()


@dp.callback_query_handler(state=Admin.confirm, text='cancel_confirm')
async def cancel_confirm(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await state.reset_state()
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await call.message.answer(f'🙋Здравствуйте <b>{call.message.from_user.full_name}</b>\n\n'
                                 f'Вы находитесь в панеле администратора\n'
                                 'Выбирете, одно из действий:',
                                 reply_markup=keyboard_admin)


@dp.callback_query_handler(user_id=admins, text_contains='confirm', state=Admin.confirm)
async def confirm(call: types.CallbackQuery, state: FSMContext):
    id_admin = call.from_user.id
    data = await state.get_data()
    id = data.get('id_lottery')
    name = data.get('name')
    description = data.get('description')
    photo = data.get('photo_lottery')
    quantity = data.get('quantity')
    price = data.get('price')
    index_id = await db3.count_lottery()
    if not index_id:                           
        await db3.add_user(id=id, id_admin=id_admin, index_id=0, name=name, description=description, photo=photo,
                           quantity=quantity, price=price)
    else:
        await db3.add_user(id=id, id_admin=id_admin, index_id=index_id, name=name, description=description, photo=photo,
                           quantity=quantity, price=price)

    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await call.message.answer(f'🙋Здравствуйте <b>{call.message.from_user.full_name}</b>\n\n'
                                 f'Вы находитесь в панеле администратора\n'
                                 'Выбирете, одно из действий:',
                                 reply_markup=keyboard_admin)
    await state.finish()


