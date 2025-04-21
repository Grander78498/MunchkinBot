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
from fastapi import Depends

current_dir = Path().absolute()
load_dotenv(current_dir.parent.parent.joinpath('.env'))

db_url = os.getenv('DB_URL')
engine = create_async_engine(db_url)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Генератор сессии обращения к БД"""

    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        yield session


AsyncGameSession = Annotated[AsyncSession, Depends(get_session)]
