from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from tg_bot.utils.utils import read_text
from tg_bot.utils.enums import Language
from tg_bot.utils.enums import KeyBoards


async def start_message(message: Message):
    builder = ReplyKeyboardBuilder()
    builder.button(text=KeyBoards.CREATE_ROOM)
    builder.button(text=KeyBoards.JOIN_GAME)
    builder.button(text=KeyBoards.SUPPORT)
    builder.button(text=KeyBoards.DONATE)
    builder.button(text=KeyBoards.PERSONAL_ACCOUNT)
    builder.adjust(4)
    await message.answer(text='Создание комнаты', reply_markup=builder.as_markup())