"""Главный файл для запуска бота."""

import asyncio
import sys
import logging
import os
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

working_dir = Path().absolute().parent
sys.path.insert(0, str(working_dir))

for name in os.listdir(working_dir):
    if working_dir.joinpath(name).is_dir():
        sys.path.insert(0, str(working_dir.joinpath(name)))

try:
    from custom_exceptions.general import EnvException
    from tg_bot.handlers.commands import router as command_router
    from tg_bot.handlers.general import router as general_router
    from tg_bot.utils.api_client import APIClient
except ImportError as e:
    raise ImportError("Ошибка при импорте внутренних модулей") from e



current_path = Path().absolute()
load_dotenv(current_path.parent.parent.joinpath(".env"), override=True)

logging.basicConfig(level=logging.INFO)
token = os.getenv("BOT_TOKEN")
if token is None:
    raise EnvException("Отсутствует переменная среды BOT_TOKEN")

bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
api_client = APIClient(base_url='http://127.0.0.1:8000')
dp = Dispatcher()
dp.include_router(command_router)
dp.include_router(general_router)


async def main() -> None:
    """Запуск бота."""
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Завершение работы бота")
