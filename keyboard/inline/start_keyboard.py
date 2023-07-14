from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup


keyboard_authorization = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Регистрация📝',
                                 callback_data='registration'),
            InlineKeyboardButton(text='Вход🚪',
                                 callback_data='entrance')
        ],
        [
            InlineKeyboardButton(text='Информация📄',
                                 callback_data='information')
        ]
    ]
)

