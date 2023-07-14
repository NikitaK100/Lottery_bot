from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

keyboard_start_lottery = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='▶Провести',
                                 callback_data='start_lottery')
        ],
        [
            InlineKeyboardButton(text="Назад",
                                 callback_data='back_admin_menu')

        ], 
        [
            InlineKeyboardButton(text="Удалить",
                                 callback_data='delete_lottery')
        ]
    ]
)

