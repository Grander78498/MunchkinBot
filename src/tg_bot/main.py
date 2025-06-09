"""Главный файл для запуска бота."""

import asyncio
import logging
import os
import sys
from pathlib import Path


working_dir = Path().absolute().parent
sys.path.insert(0, str(working_dir))

for name in os.listdir(working_dir):
    if working_dir.joinpath(name).is_dir():
        sys.path.insert(0, str(working_dir.joinpath(name)))

try:
    from tg_bot.handlers.commands import router as command_router
    from tg_bot.handlers.general import router as general_router
    from tg_bot.utils.api_client import APIClient
    from tg_bot.settings import get_bot, get_dispatcher
except ImportError as e:
    raise ImportError("Ошибка при импорте внутренних модулей") from e

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    """Запуск бота."""
    dp = get_dispatcher()
    bot = get_bot()
    dp.include_router(command_router)
    dp.include_router(general_router)
    async with APIClient(base_url="http://127.0.0.1:8000") as _:
        await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Завершение работы бота")
