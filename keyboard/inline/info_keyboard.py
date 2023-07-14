from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


keyboard_information = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='🔙Назад',
                                 callback_data='back')
        ]
    ]
)