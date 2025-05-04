from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from tg_bot.utils.utils import read_text
from tg_bot.utils.enums import Language


async def start_message(message: Message):
    # inline_builder = InlineKeyboardBuilder()
    reply_builder = ReplyKeyboardBuilder()
    reply_builder.button(text="Создать игру")
    reply_builder.button(text="Присоединиться")
    reply_builder.button(text="Личный кабинет")
    reply_builder.button(text="Личный кабинет родителя")

    # inline_builder.button(text='➕ Добавить бота в группу',
    #                       url=f'https://t.me/{(await bot.get_me()).username}?startgroup=true')
    # await message.answer(read_text("start", Language.RU), reply_markup=inline_builder.as_markup())
    await message.answer(read_text("start", Language.RU), reply_markup=reply_builder.as_markup())