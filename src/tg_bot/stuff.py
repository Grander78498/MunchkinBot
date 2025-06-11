"""Для функций, которые будут манипулировать состояниями разных пользователей."""

from tg_bot.messages import start_message
from tg_bot.settings import get_bot, get_dispatcher

dp = get_dispatcher()
bot = get_bot()


async def deleted_from_game(user_id: int) -> None:
    """Принудительная смена состояния при удалении из игры.

    Параметры:
        user_id: int - id пользователя, у которого сменяется состояние
    """
    state = dp.fsm.get_context(bot, chat_id=user_id, user_id=user_id)
    await start_message(
        state,
        text="Активная игра была удалена или вас забанили",
        bot=bot,
        user_id=user_id,
    )
