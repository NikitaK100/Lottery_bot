from aiogram import types
from loader import dp
from states.buy_coin import GetCoin
from aiogram.dispatcher.storage import FSMContext
from utils.db_api.schemas import quick_commands as db2
# from utils.misc.qiwi import NotEnoughMoney, NotPaymentFound, Payment
from aiogram.utils.markdown import hlink, hcode
from data import config
from keyboard.inline.check_payment import check_payment_coins
from keyboard.inline.keyboard_account import keyboard_add_money

# Покупка монет через api qiwi

@dp.callback_query_handler(text='pay')
async def show_ineoices(call: types.CallbackQuery):
    user_id = call.from_user.id
    wallet = await db2.select_user(id=user_id)
    await call.answer()
    await call.message.edit_text(f'<b>В ДАННЫЙ МОМЕНТ ОПРЕАЦИЯ НЕДОСТУПНА</b>\n\n'
                                f'Баланс: <b>{wallet.wallet}</b> монет \n\n'
                                f'🔻Выберите, что хотите сделать🔻',
                                reply_markup=keyboard_add_money)
    

# @dp.callback_query_handler(text='pay')
# async def show_invoices(call: types.CallbackQuery):
#     await call.answer()
#     await call.message.edit_text('-----------------------------------------------------------------------------\n\n'
#                                  'На сколько вы хоите пополнить счёт?\n'
#                                  '(укажите число):\n\n'
#                                  '-----------------------------------------------------------------------------')
#     await GetCoin.get_coin.set()


# @dp.message_handler(state=GetCoin.get_coin)
# async def get_quantity_coins(message: types.Message, state: FSMContext):
#     quantity = int(message.text)
#     payment = Payment(amount=quantity)
#     payment.create()
#     await state.update_data(
#         {
#             'payment': payment, 
#             'quantity': quantity
#         }
#     )

#     await message.answer('\n'.join(
#         [f"Сумма платежа составляет {quantity} RUB",
#          '',
#          "Оплатите по номеру телефона или по адресу",
#          hlink(config.qiwi_phone, url=payment.invoice),
#          'Обязательно платите по ID платежа',
#          hcode(payment.id)]), reply_markup=check_payment_coins)
#     await GetCoin.confirm.set()


# @dp.callback_query_handler(state=GetCoin.confirm, text='cancellation')
# async def cancel_check_payment(call: types.CallbackQuery, state: FSMContext):
#     user_id = call.from_user.id
#     name = call.from_user.full_name
#     wallet = await db2.select_user(id=user_id)
#     await call.answer()
#     await call.message.edit_text(f'Добро пожаловать <b>{name}</b>\n\n'
#                                  f'Баланс: <b>{wallet.wallet}</b> монет \n\n'
#                                  f'🔻Выберите, что хотите сделать🔻',
#                                  reply_markup=keyboard_add_money)
#     await state.finish()


# @dp.callback_query_handler(state=GetCoin.confirm, text='end_payment')
# async def end_payment(call: types.CallbackQuery, state: FSMContext):
#     await call.answer()
#     data = await state.get_data()
#     user_id = call.from_user.id
#     name = call.from_user.full_name
#     wallet = await db2.select_user(id=user_id)
#     payment: Payment = data.get('payment')
#     try:
#         payment.check_payment()
#     except NotPaymentFound:
#         await call.message.answer('Транзакция не найдена')
#         return
#     except NotEnoughMoney:
#         await call.message.answer('Оплаченная сумма меньше необходимой')
#         return
#     else:
#         coin = data.get('quantity')
#         # print(coin)
#         await db2.update_wallet(id=user_id, wallet=wallet.wallet + coin)
#         await call.message.edit_text('Вы успешно пополнили счёт!\n\n'
#                                     f'Добро пожаловать <b>{name}</b>\n\n'
#                                     f'Баланс: <b>{wallet.wallet + coin}</b> монет \n\n'
#                                     f'🔻Выберите, что хотите сделать🔻',
#                                     reply_markup=keyboard_add_money)
#         await state.finish()

