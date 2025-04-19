import os

from pathlib import Path
from typing import AsyncGenerator

from dotenv import load_dotenv
from sqlmodel import (
    SQLModel,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    AsyncEngine
)
from sqlalchemy.orm import (
    registry
)

class SQLModel_GAME(SQLModel, registry=registry()):
    pass


class SQLModel_CARDS(SQLModel, registry=registry()):
    pass

current_dir = Path().absolute()
load_dotenv(current_dir.parent.parent.joinpath('.env'))

db_game_url = os.getenv('DB_GAME_URL')
db_cards_url = os.getenv('DB_CARDS_URL')
game_engine = create_async_engine(db_game_url)
cards_engine = create_async_engine(db_cards_url)


async def create_game_tables():
    async with game_engine.begin() as conn:
        await conn.run_sync(SQLModel_GAME.metadata.create_all)


async def create_cards_tables():
    async with cards_engine.begin() as conn:
        await conn.run_sync(SQLModel_CARDS.metadata.create_all)


async def get_game_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(game_engine, expire_on_commit=False)
    async with async_session() as session:
        yield session


async def get_cards_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(game_engine, expire_on_commit=False)
    async with async_session() as session:
        yield session