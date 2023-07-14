from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton

keyboard_back = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='🔙Назад',
                                 callback_data='entrance')
        ]
    ]
)