import os

from pathlib import Path
from typing import AsyncGenerator

from dotenv import load_dotenv
from sqlmodel import (
    SQLModel,
    Field,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

current_dir = Path().absolute()
load_dotenv(current_dir.parent.parent.joinpath('.env'))

db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')

db_url = f'postgresql+asyncpg://{db_user}:{db_password}@{db_host}/{db_name}'
engine = create_async_engine(db_url)


class User(SQLModel, table=True):
    __tablename__ = 'tg_user'

    tg_id: int = Field(primary_key=True)
    user_name: str = Field(unique=True)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        yield session
