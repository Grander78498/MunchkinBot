from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


class Settings():
    def __new__(cls, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(Settings, cls).__new__(cls, **kwargs)
        return cls.instance
    
    def __init__(self, bot: Bot | None = None, dp: Dispatcher | None = None):
        self.bot = bot
        self.dp = dp


def get_settings(token: str | None = None) ->  Settings:
    settings = Settings()
    if settings.bot is None and token is not None:
        settings.bot = Bot(
            token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        settings.dp = Dispatcher()
    return settings