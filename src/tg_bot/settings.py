"""Хранение бота и диспетчера."""

import os
from pathlib import Path
from functools import lru_cache

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from custom_exceptions.general import EnvException


current_path = Path().absolute()
load_dotenv(current_path.parent.parent.joinpath(".env"), override=True)

token = os.getenv("BOT_TOKEN")
if token is None:

    raise EnvException("Отсутствует переменная среды BOT_TOKEN")


@lru_cache
def get_bot() -> Bot:
    """Получение объекта бота."""
    return Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


@lru_cache
def get_dispatcher() -> Dispatcher:
    """Получение объекта диспетчера."""
    return Dispatcher()
