from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

keyboard_admin_back = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Назад',
                                 callback_data='admin_back')
        ]
    ]
)