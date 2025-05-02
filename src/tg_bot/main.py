"""Главный файл для запуска бота."""

import asyncio
import logging
import os
from pathlib import Path
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from dotenv import load_dotenv
from tg_bot.utils.api_client import APIClient
from custom_exceptions import EnvException, TGException

current_path = Path().absolute()
load_dotenv(current_path.parent.parent.joinpath(".env"), override=True)

logging.basicConfig(level=logging.INFO)
token = os.getenv("BOT_TOKEN")
if token is None:
    raise EnvException("Отсутствует переменная среды BOT_TOKEN")

bot = Bot(token=token)
dp = Dispatcher()
api_client = APIClient("http://127.0.0.1:8000")


@dp.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    """Обработка команды start."""
    user = message.from_user
    if user is None:
        raise TGException("Ошибка при получении отправителя сообщения")
    result = api_client.save_user(user.id, user.username, user.full_name)
    await message.answer(result["msg"])


async def main() -> None:
    """Запуск бота."""
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
