"""
Реализует обращения к базам данных.
"""

import os

from pathlib import Path
from typing import Any, AsyncGenerator, Annotated

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (AsyncSession, create_async_engine,
                                    async_sessionmaker)
from sqlalchemy import MetaData
from sqlmodel import SQLModel, Relationship
from fastapi import Depends

from custom_exceptions.general import EnvException


class CustomSQLModel(SQLModel):
    """
    Надстройка над базовым SQLModel,
    чтобы встроить автоматическое наименование constraint
    """

    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_`%(constraint_name)s`",
            "fk":
            "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s"
        })


current_dir = Path().absolute()
load_dotenv(current_dir.parent.parent.joinpath('.env'))

db_url = os.getenv('DB_URL')
if db_url is None:
    raise EnvException('Отсутствует переменная среды DB_URL')
engine = create_async_engine(db_url)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Генератор сессии обращения к БД"""

    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        yield session


def lazy_relationship(*args, **kwargs) -> Any:  #type: ignore [no-untyped-def]
    """Relationship, который легче использовать в асинхронных запросах"""
    return Relationship(*args,
                        sa_relationship_kwargs={'lazy': 'selectin'},
                        **kwargs)


AsyncGameSession = Annotated[AsyncSession, Depends(get_session)]
