from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

keyboard_admin = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='📝Создать лотерею',
                                 callback_data='create_lottery')
        ],
        [
            InlineKeyboardButton(text='🥁Начать розыгрыш',
                                 callback_data='winner')
        ],
        [
            InlineKeyboardButton(text='📕Список участников',
                                 callback_data='list_everething_participants')
        ]
    ]
)