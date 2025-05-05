"""
Таблицы для хранения информации, связанной с телеграмом.

(может, переименовать в telegram.py?)
"""

from typing import TYPE_CHECKING

from sqlmodel import Field
from sqlalchemy import BigInteger, Column

from backend.database import CustomSQLModel, lazy_relationship

if TYPE_CHECKING:
    from backend.database.game import Munchkin, Game


class User(CustomSQLModel, table=True):
    """Пользователь."""

    __tablename__ = "tg_user"

    tg_id: int = Field(
        sa_column=Column(
            BigInteger(), primary_key=True, autoincrement=False, nullable=False
        )
    )
    user_name: str = Field(unique=True, max_length=32)
    full_name: str = Field(unique=True, max_length=128)

    munchkins: list["Munchkin"] = lazy_relationship(back_populates="user", cascade_delete=True)
    games: list["Game"] = lazy_relationship(back_populates="creator", cascade_delete=True)
