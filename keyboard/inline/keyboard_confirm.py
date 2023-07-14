from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

confirmation_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='✅Подтвердить',
                                 callback_data='confirm'), 
                                 
            InlineKeyboardButton(text='❌Отменить', 
                                callback_data='cancel_confirm')
        ]
    ]
)