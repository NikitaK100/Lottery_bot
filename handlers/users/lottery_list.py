from aiogram import types
from keyboard.inline.keyboard_account import keyboard_add_money
from loader import dp, bot
from utils.db_api.schemas import commands_lottery as db3
from utils.db_api.schemas import quick_commands as db2
from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.types.input_media import InputMedia
from keyboard.inline.keyboards_mixin import confirm_keyboards

data_key = CallbackData('paginator', 'key', 'page')

# пагинатор лотерей 


async def max_page():
    count = await db3.count_lottery()
    return count


async def get_page(number_page):
    cards = await db3.select_id()
    list_lottery = [[] for lottery in range(await max_page())]   # создаю вложенные их кол-во зависит от кол-ва лотерей
    number = 0
    for card in cards:                                           # перебрал список со списками 
        list_lottery[number].append(card.name)
        list_lottery[number].append(card.description)
        list_lottery[number].append(card.price)
        list_lottery[number].append(card.photo)
        number += 1                                              # распределяет значения по вложеным спискам 
    text = f'<b>{list_lottery[number_page][0]}</b>\n\n {list_lottery[number_page][1]}\n\nЦена: {list_lottery[number_page][2]}🪙'
    photo = f'{list_lottery[number_page][3]}'
    return {'text': text, 'photo': photo}    


async def get_id(index):
    '''
    Эта функция принимает индекс(в будущем index=curren_page) как аргумент и отдаёт id лотереи при нажатии 
    '''                  
    db_id = await db3.select_id()
    list_id = []
    for data_id in db_id:
        list_id.append(data_id.id)
    return list_id[index]


async def get_keyboard_page(max_pages: int, key='book',  page: int = 0):

    """
    Эта функция возвращает динамическую клавитуру(пагинация)
    и связывает переданные значения с CallbackData,
    к ним удобно обращатся в будущем
    """

    previous_page = page - 1
    previous_text = '<<<'

    current_text = '✅Выбрать'

    next_page = page + 1
    next_text = '>>>'

    markup = InlineKeyboardMarkup()

    if previous_page > -1:          
        markup.insert(
            InlineKeyboardButton(
                text=previous_text,
                callback_data=data_key.new(key=key, page=previous_page)
            )
        )

    markup.insert(
        InlineKeyboardButton(
            text=current_text,
            callback_data=data_key.new(key=key, page=f'{await get_id(page)}')  # получили id лотереи 
        )
    )

    if next_page < max_pages:
        markup.insert(
            InlineKeyboardButton(
                text=next_text,
                callback_data=data_key.new(key=key, page=next_page)
            )
        )

    markup.insert(
        InlineKeyboardButton(
            text='Главная',
            callback_data=data_key.new(key=key, page='back')
        )
    )

    return markup


@dp.callback_query_handler(data_key.filter(page='back'))
async def previous_level(call: types.CallbackQuery):
    await call.answer()
    user_id = call.from_user.id
    name = call.from_user.full_name
    wallet = await db2.select_user(id=user_id)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await call.message.answer(f'Добро пожаловать <b>{name}</b>\n\n'
                                f'Баланс: <b>{wallet.wallet}</b> монет \n\n'
                                f'🔻Выберите, что хотите сделать🔻',
                                reply_markup=keyboard_add_money)


@dp.callback_query_handler(text='lottery')
async def everything(call: types.CallbackQuery):
    card_lottery = await get_page(0)
    keyboard = await get_keyboard_page(await max_page())
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await bot.send_photo(chat_id=call.message.chat.id, photo=card_lottery['photo'], 
    caption=card_lottery['text'], reply_markup=keyboard)


@dp.callback_query_handler(data_key.filter(key='book'))
async def all_requests(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer()
    current_page = int(callback_data.get('page'))
    if current_page > 1000:                              # если в current_page было передано число больше 1000 тогда это номер лотереи
        await state.update_data(                         # P.S. каждая лотерея имеет свой индекс(номер страницы)
            {
                'client_id': call.from_user.id,
                'lottery_id': current_page
            }
        )
        
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await call.message.answer('Подтвердите покупку:',
                                 reply_markup=confirm_keyboards('buy', 'cancel_buy'))
        await state.set_state('buying_lottery')

    else:                                                
        card_lottery = await get_page(int(current_page))
        markup = await get_keyboard_page(max_pages=await max_page(), page=int(current_page))
        photo = InputMedia(type='photo', media=card_lottery['photo'], caption=card_lottery['text'])
        await call.message.edit_media(photo, markup)



    




