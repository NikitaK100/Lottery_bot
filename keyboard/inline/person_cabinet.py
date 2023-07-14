from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

keyboard_back_to_cabinet = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
           InlineKeyboardButton(text='🚪Личный кабинет',
                                callback_data='entrance')
        ]
    ]
)