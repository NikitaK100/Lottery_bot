from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp

# Раздел помощи пользователям и контакты тех поддержки

@dp.message_handler(Command('help', prefixes='!/'))
async def helping(message: types.Message):
    await message.reply('Если возникли проблемы с ботом то 90%\n'
                        'проблем решаются командой /start\n\n'
                        'Если проблема имеет тотальный характер\n'
                        'свяжитесь со мной :\n'
                        '@Some_user3490583420932095')
