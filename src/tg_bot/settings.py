"""Настройки бота."""

from functools import lru_cache

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    """Переменные окружения."""

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Переопределение порядка импорта переменных окружения."""
        return (
            dotenv_settings,
            env_settings,
            init_settings,
            file_secret_settings,
        )

    model_config = SettingsConfigDict(env_file=".env")

    bot_token: str
    api_url: str


@lru_cache
def get_settings() -> Settings:
    """Получение переменных окружения."""
    return Settings()


@lru_cache
def get_bot() -> Bot:
    """Получение объекта бота."""
    return Bot(
        token=get_settings().bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )


@lru_cache
def get_dispatcher() -> Dispatcher:
    """Получение объекта диспетчера."""
    return Dispatcher()
