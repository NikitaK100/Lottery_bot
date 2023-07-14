from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


keyboard_list = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text='💲Купить билет',
                                 callback_data='buy_billet'),
            InlineKeyboardButton(text='🔙Вернуться',
                                 callback_data='exit')
        ]
    ]
)

keyboard_back_pc = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text='✅Подтвердить',
                                 callback_data='back_pc')

        ]
    ]
)
