from aiogram import types
from random import randint
from data.config import admins
from keyboard.inline.admin_keyboard.admin_keyboard import keyboard_admin
from keyboard.inline.admin_keyboard.keyboard_start_lottery import keyboard_start_lottery
from loader import dp, bot
from states.start_lottery import StartLottery
from aiogram.dispatcher.storage import FSMContext
from utils.db_api.schemas import commands_lottery as db3
from utils.db_api.schemas import lottery_participants as db4
import secrets
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


data_winner = CallbackData('who_winner', 'key', 'lottery_id')


async def get_keyboard_list_lotterys(key='lottery_id', lottery_id: str='0'):

    list_participants_all_lotterys = [{'id': list_participants.id, 
                                       'name': list_participants.name} for  list_participants 
                                       in await db3.select_all()]


    markup = InlineKeyboardMarkup(row_width=1)
    for number_lottery in list_participants_all_lotterys:
        lottery_id = number_lottery
        markup.insert(
            InlineKeyboardButton(
                text=number_lottery['name'],
                callback_data=data_winner.new(key=key, lottery_id=lottery_id['id'])
            )
        )
    markup.insert(
            InlineKeyboardButton(
                text='Назад',
                callback_data='back_admin_menu')
            )
    return markup


@dp.callback_query_handler(user_id=admins, text='winner')
async def select_lottery_who_winner(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text("Выбирите лотерею которую хотите провести:", reply_markup=await get_keyboard_list_lotterys())
    await StartLottery.get_number_lottery.set()


@dp.callback_query_handler(data_winner.filter(key='lottery_id'), state=StartLottery.get_number_lottery)
async def get_data(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer()
    number_lottery = int(callback_data.get('lottery_id'))
    count = await db4.count_users(lottery_id=number_lottery)
    data_db_3 = await db3.select_id_lottery(id=number_lottery)

    await state.update_data(
        {
            'id_lottery': number_lottery
        }
    )

    await call.message.edit_text(f'Лотерея №{number_lottery}\n'
                        f'Максимальное кол_во участников: {data_db_3.quantity}\n'
                        f'Набрано: {count}',
                        reply_markup=keyboard_start_lottery)
    await StartLottery.select_winner.set()


@dp.callback_query_handler(text='delete_lottery', state=StartLottery.select_winner)
async def delete_lottery(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    await db3.delete_lottery(id=data.get('id_lottery'))
    await call.message.edit_text('<b>Лотерея успешно удалена</b>\n\n'
                                 f'🙋Здравствуйте <b>{call.from_user.full_name}</b>\n\n'
                                 f'Вы находитесь в панеле администратора\n'
                                'Выбирете, одно из действий:',
                                reply_markup=keyboard_admin)
    await state.reset_state()


@dp.callback_query_handler(user_id=admins, text='start_lottery', state=StartLottery.select_winner)
async def select_winner_lottery(call: types.CallbackQuery, state: FSMContext):

    await call.answer()

    data_lottery = await state.get_data()
    lottery_id_from_state = data_lottery.get('id_lottery')
    cycle = await db4.select_all_lottery_users(lottery_id=lottery_id_from_state)
    count = await db4.count_users(lottery_id=lottery_id_from_state)
    list_participants = []
    select_random_winner = randint(0, count-1)           

    for names in cycle:
        list_participants.append([names.name, names.id])

    await call.message.answer(f'Список участников:\n'
                              f'{tuple(list_participants)}')

    winner = list_participants[select_random_winner]

    create_code = secrets.token_hex(8)                                       # генерирует токе из 8 симвволов назвав который, победитель сможет получить приз

    await call.message.answer(f'Победитель:\n'                                # говорим администратору кто победил и токен 
                              f'{tuple(winner)}\n\n'
                              f'Секретный код выйгрыша: <b>{create_code}</b>')
    # отправлем сообщение(по id) нашему победителю 
    await bot.send_message(chat_id=winner[1], text=f'Вы стали победителем лотереи №{lottery_id_from_state}🤑\n'
                                                   f'Секретный код выйгрыша: <b>{create_code}</b>🤫\n\n'
                                                   f'Сообщите этот код администратору бота и получите выйгрыш\n'
                                                   f'Администратор: @Aki_256')
    await db3.delete_lottery(id=int(lottery_id_from_state))
    await state.finish()


@dp.callback_query_handler(user_id=admins, text='back_admin_menu', state=StartLottery)
async def exit(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await state.reset_state()
    await call.message.edit_text(f'🙋Здравствуйте <b>{call.from_user.full_name}</b>\n\n'
                              f'Вы находитесь в панеле администратора\n'
                              'Выбирете, одно из действий:',
                              reply_markup=keyboard_admin)


