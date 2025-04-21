"""
Модели для базы данных, связанной с процессом игры.
Все классы, представленные здесь, являются либо таблицами,
либо "абстрактными" классами
"""

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, BigInteger


class User(SQLModel, table=True):
    """Пользователь"""

    __tablename__ = 'tg_user'

    tg_id: int = Field(
        sa_column=Column(BigInteger(), primary_key=True, autoincrement=False))
    user_name: str = Field(unique=True, max_length=32)
    full_name: str = Field(unique=True, max_length=128)


class Group(SQLModel, table=True):
    """Телеграм группа"""

    __tablename__ = 'tg_group'

    tg_id: int = Field(
        sa_column=Column(BigInteger(), primary_key=True, autoincrement=False))
    name: str = Field(unique=True, max_length=32)

    games: list["Game"] = Relationship(back_populates="group")


class Game(SQLModel, table=True):
    """Информация об игровой партии"""

    id: int | None = Field(default=None, primary_key=True)
    group_id: int = Field(foreign_key="tg_group.tg_id")
    on_going: bool
    current_player_number: int

    group: Group = Relationship(back_populates="games")


# class PossibleGenders(SQLModel, table = True):
#     pass

# class Stats(SQLModel, table = True):
#     pass

# class StatsType(SQLModel, table = True):
#     pass

# class MunchkinStats(SQLModel, table = True):
#     pass

# class MunchkinItem(SQLModel, table = True):
#     pass

# class Munchkin(SQLModel, table = True):
#     pass

# class MunchkinCombat(SQLModel, table = True):
#     pass

# class MonsterCombat(SQLModel, table = True):
#     pass

# class Combat(SQLModel, table = True):
#     pass

# class MunchkinCards(SQLModel, table = True):
#     pass

# class Monster(SQLModel, table = True):
#     pass

# class UndeadType(SQLModel, table = True):
#     pass
