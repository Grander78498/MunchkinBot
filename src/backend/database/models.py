"""
Модели для базы данных, связанной с процессом игры.
Все классы, представленные здесь, являются либо таблицами,
либо "абстрактными" классами
"""

from enum import Enum

from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint
from sqlalchemy import Column, BigInteger, SmallInteger
from sqlalchemy.dialects.postgresql import ENUM


def LazyRelationship(*args, **kwargs):
    return Relationship(*args, sa_relationship_kwargs={'lazy': 'selectin'}, **kwargs)


class Gender(str, Enum):
    MALE = 'male'
    FEMALE = 'female'


class TurnType(str, Enum):
    KICK_DOOR = 'kick_door'
    LOOK_TROUBLE = 'look_trouble'
    LOOT_ROOM = 'loot_room'
    CHARITY = 'charity'
    COMBAT = 'combat'


class MunchkinCombat(SQLModel, table=True):
    munchkin_id: int | None = Field(default=None, primary_key=True, foreign_key="munchkin.id")
    combat_id: int | None = Field(default=None, primary_key=True, foreign_key="combat.id")
    modifier: int = Field(sa_column=Column(SmallInteger()))
    runaway_bonus: int = Field(sa_column=Column(SmallInteger()))
    is_helping: bool


class UserBase(SQLModel):
    tg_id: int


class User(UserBase, table=True):
    
    """Пользователь"""

    __tablename__ = 'tg_user'

    tg_id: int = Field(
        sa_column=Column(BigInteger(), primary_key=True, autoincrement=False))
    user_name: str = Field(unique=True, max_length=32)
    full_name: str = Field(unique=True, max_length=128)

    munchkins: list["Munchkin"] = LazyRelationship(back_populates="user")


class GroupBase(SQLModel):
    tg_id: int


class Group(GroupBase, table=True):
    """Телеграм группа"""

    __tablename__ = 'tg_group'

    tg_id: int = Field(
        sa_column=Column(BigInteger(), primary_key=True, autoincrement=False))
    name: str = Field(unique=True, max_length=32)

    games: list["Game"] = LazyRelationship(back_populates="group")


class Game(SQLModel, table=True):
    """Информация об игровой партии"""

    id: int | None = Field(default=None, primary_key=True)
    group_id: int = Field(foreign_key="tg_group.tg_id")
    on_going: bool = Field(default=False)
    current_player_number: int = Field(default=-1)

    group: Group = Relationship(back_populates="games")

    munchkins: list["Munchkin"] = LazyRelationship(back_populates="game")
    combats: list["Combat"] = LazyRelationship(back_populates="game")


class Munchkin(SQLModel, table=True):
    """Информация о манчкине"""

    __table_args__ = (
        UniqueConstraint("user_id", "game_id"),
    )

    id: int | None = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="tg_user.tg_id")
    game_id: int = Field(foreign_key="game.id")
    
    gender: Gender = Field(default=Gender.MALE, sa_column=Column(ENUM(Gender)))
    number: int = Field(default=-1, sa_column=Column(SmallInteger()))
    level: int = Field(default=1, sa_column=Column(SmallInteger()))
    strength: int = Field(default=1, sa_column=Column(SmallInteger()))
    luck: int = Field(default=0, sa_column=Column(SmallInteger()))
    runaway_bonus: int = Field(default=0, sa_column=Column(SmallInteger()))

    user: User = LazyRelationship(back_populates="munchkins")
    game: Game = LazyRelationship(back_populates="munchkins")

    turns: list["Turn"] = LazyRelationship(back_populates="munchkin")
    combats: list["Combat"] = LazyRelationship(back_populates="munchkins", link_model=MunchkinCombat)


class Turn(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    
    munchkin_id: int = Field(foreign_key="munchkin.id")
    turn_type: TurnType = Field(sa_column=Column(ENUM(TurnType)))

    munchkin: Munchkin = LazyRelationship(back_populates="turns")


class Combat(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    game_id: int = Field(foreign_key="game.id")
    difference: int = Field(sa_column=Column(SmallInteger()))
    munchkin_can_join: bool
    monster_can_join: bool
    is_active: bool
    is_runaway: bool
    
    game: Game = LazyRelationship(back_populates="combats")

    munchkins: list[Munchkin] = LazyRelationship(back_populates="combats", link_model=MunchkinCombat)


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
