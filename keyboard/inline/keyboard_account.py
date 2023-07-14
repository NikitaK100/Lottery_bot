from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

keyboard_add_money = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="💵Пополнить",
                                 callback_data='pay'),

            InlineKeyboardButton(text='🎰Лотереи',
                                 callback_data='lottery')
        ], 
        [
            InlineKeyboardButton(text='Мои лотереи', 
                                 callback_data='my_lottery')
        ]
    ]
)

