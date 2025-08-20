from aiogram import Router, F
from aiogram.types import Message

start_router = Router()

from gigachat import GigaChat

@start_router.message(F.text == 'start')
async def cmd_start_3(message: Message):
    await message.answer('Запуск сообщения по команде start')