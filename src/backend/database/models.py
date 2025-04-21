"""
Модели для базы данных, связанной с процессом игры.
Все классы, представленные здесь, являются либо таблицами,
либо "абстрактными" классами
"""

from enum import Enum

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM


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


class User(SQLModel, table=True):
    
    """Пользователь"""

    __tablename__ = 'tg_user'

    tg_id: int = Field(
        sa_column=Column(BigInteger(), primary_key=True, autoincrement=False))
    user_name: str = Field(unique=True, max_length=32)
    full_name: str = Field(unique=True, max_length=128)

    munchkins: list["Munchkin"] = Relationship(back_populates="user")


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

    munchkins: list["Munchkin"] = Relationship(back_populates="game")
    combats: list["Combat"] = Relationship(back_populates="game")


class Munchkin(SQLModel, table=True):
    """Информация о манчкине"""

    id: int | None = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="tg_user.tg_id")
    game_id: int = Field(foreign_key="game.id")
    
    gender: Gender = Field(sa_column=Column(ENUM(Gender)))
    number: int = Field(sa_column=Column(SmallInteger()))
    level: int = Field(sa_column=Column(SmallInteger()))
    strength: int = Field(sa_column=Column(SmallInteger()))
    luck: int = Field(sa_column=Column(SmallInteger()))
    runaway_bonus: int = Field(sa_column=Column(SmallInteger()))

    user: User = Relationship(back_populates="munchkins")
    game: Game = Relationship(back_populates="munchkins")

    turns: list["Turn"] = Relationship(back_populates="turn")
    combats: list["Combat"] = Relationship(back_populates="munchkins", link_model=MunchkinCombat)


class Turn(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    
    munchkin_id: int = Field(foreign_key="munchkin.id")
    turn_type: TurnType = Field(sa_column=Column(ENUM(TurnType)))

    munchkin: Munchkin = Relationship(back_populates="turns")


class Combat(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    game_id: int = Field(foreign_key="game.id")
    difference: int = Field(sa_column=Column(SmallInteger()))
    munchkin_can_join: bool
    monster_can_join: bool
    is_active: bool
    is_runaway: bool
    
    game: Game = Relationship(back_populates="combats")

    munchkins: list[Munchkin] = Relationship(back_populates="combats", link_model=MunchkinCombat)


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
