"""Для функций, которые будут манипулировать состояниями разных пользователей"""


from aiogram import Bot

from tg_bot.messages import start_message
from tg_bot.settings import get_settings

settings = get_settings()


async def deleted_from_game(bot: Bot,  user_id: int):
    state = settings.dp.fsm.get_context(bot, chat_id=user_id, user_id=user_id)
    await start_message(state, 
                        text="Активная игра была удалена или вас забанили",
                        bot=bot,
                        user_id=user_id)