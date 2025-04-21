"""
Реализует обращения к базам данных.
"""

import os

from pathlib import Path
from typing import AsyncGenerator, Annotated

from dotenv import load_dotenv
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import (AsyncSession, create_async_engine,
                                    async_sessionmaker, AsyncEngine)
from sqlalchemy.orm import registry
from fastapi import Depends


class SQLModelGame(SQLModel, registry=registry()):
    """Класс для метаданных БД игрового процесса"""


class SQLModelCards(SQLModel, registry=registry()):
    """Класс для метаданных БД карточек"""


current_dir = Path().absolute()
load_dotenv(current_dir.parent.parent.joinpath('.env'))

db_game_url = os.getenv('DB_GAME_URL')
db_cards_url = os.getenv('DB_CARDS_URL')
game_engine = create_async_engine(db_game_url)
cards_engine = create_async_engine(db_cards_url)


async def create_game_tables():
    """Создаёт таблицы в БД игрового процесса на основе метаданных"""

    async with game_engine.begin() as conn:
        await conn.run_sync(SQLModelGame.metadata.create_all)


async def create_cards_tables():
    """Создаёт таблицы в БД карточек на основе метаданных"""

    async with cards_engine.begin() as conn:
        await conn.run_sync(SQLModelCards.metadata.create_all)


async def get_game_session() -> AsyncGenerator[AsyncSession, None]:
    """Генератор сессии обращения к БД игрового процесса"""

    async_session = async_sessionmaker(game_engine, expire_on_commit=False)
    async with async_session() as session:
        yield session


async def get_cards_session() -> AsyncGenerator[AsyncSession, None]:
    """Генератор сессии обращения к БД карточек"""

    async_session = async_sessionmaker(game_engine, expire_on_commit=False)
    async with async_session() as session:
        yield session


AsyncGameSession = Annotated[AsyncSession, Depends(get_game_session)]
AsyncCardsSession = Annotated[AsyncSession, Depends(get_cards_session)]
