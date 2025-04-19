from sqlmodel import (
    Field
)
from backend.models import SQLModel_GAME


class User(SQLModel_GAME, table=True):
    __tablename__ = 'tg_user'

    tg_id: int = Field(primary_key=True)
    user_name: str = Field(unique=True, max_length=32)
    full_name: str = Field(unique=True, max_length=128)


class Group(SQLModel_GAME, table = True):
    __tablename__ = 'tg_group'

    tg_id: int = Field(primary_key=True)
    name: str = Field(unique=True, max_length=32)


# class Game(SQLModel_GAME, table = True):
#     pass


# class PossibleGenders(SQLModel_GAME, table = True):
#     pass


# class Stats(SQLModel_GAME, table = True):
#     pass


# class StatsType(SQLModel_GAME, table = True):
#     pass


# class MunchkinStats(SQLModel_GAME, table = True):
#     pass


# class MunchkinItem(SQLModel_GAME, table = True):
#     pass


# class Munchkin(SQLModel_GAME, table = True):
#     pass


# class MunchkinCombat(SQLModel_GAME, table = True):
#     pass


# class MonsterCombat(SQLModel_GAME, table = True):
#     pass


# class Combat(SQLModel_GAME, table = True):
#     pass


# class MunchkinCards(SQLModel_GAME, table = True):
#     pass


# class Monster(SQLModel_GAME, table = True):
#     pass


# class UndeadType(SQLModel_GAME, table = True):
#     pass