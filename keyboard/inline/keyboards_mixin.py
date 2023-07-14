from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def confirm_keyboards(callback_data_1, callback_data_2):
    keyboard_confirm = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='✅Подтвердить',
                                        callback_data=callback_data_1)
            ], 
            [
                InlineKeyboardButton(text='❌Отмена', 
                                        callback_data=callback_data_2)
            ]
        ]
    )
    return keyboard_confirm