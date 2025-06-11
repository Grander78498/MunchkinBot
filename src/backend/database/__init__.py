"""Реализует обращения к базам данных."""

import os
from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Annotated, Any

from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel import Relationship, SQLModel

from custom_exceptions.general import EnvException


class CustomSQLModel(SQLModel):
    """Надстройка над базовым SQLModel.

    чтобы встроить автоматическое наименование constraint
    """

    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_`%(constraint_name)s`",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


current_dir = Path().absolute()
load_dotenv(current_dir.parent.parent.joinpath(".env"))

db_url = os.getenv("DB_URL")
if db_url is None:
    raise EnvException("Отсутствует переменная среды DB_URL")
engine = create_async_engine(db_url)


async def get_session() -> AsyncGenerator[AsyncSession]:
    """Генератор сессии обращения к БД."""
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        yield session


def lazy_relationship(
    *,
    back_populates: str | None = None,
    sa_relationship_args: list[Any] | None = None,
    sa_relationship_kwargs: dict[str, Any] | None = None,
    **kwargs: Any,
) -> Any:
    """Перегруженная функция Relationship с дополнительными параметрами."""
    if sa_relationship_kwargs is None:
        sa_relationship_kwargs = {}

    sa_relationship_kwargs.setdefault("lazy", "selectin")

    return Relationship(
        back_populates=back_populates,
        sa_relationship_args=sa_relationship_args,
        sa_relationship_kwargs=sa_relationship_kwargs,
        **kwargs,
    )


AsyncGameSession = Annotated[AsyncSession, Depends(get_session)]
