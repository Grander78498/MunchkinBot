from typing import TYPE_CHECKING

from sqlmodel import Field
from sqlalchemy import UniqueConstraint, SmallInteger
from sqlalchemy.dialects.postgresql import ENUM

from backend.database import CustomSQLModel, lazy_relationship
from backend.database.link_models import MunchkinCard, MunchkinCombat, MunchkinItem
from backend.database.enums import Gender, TurnType

if TYPE_CHECKING:
    from backend.database.users import User, Group
    from backend.database.cards import GameCard, GameItem


class Game(CustomSQLModel, table=True):
    """Информация об игровой партии"""

    id: int | None = Field(default=None, primary_key=True)
    group_id: int = Field(foreign_key="tg_group.tg_id")
    on_going: bool = Field(default=False)
    current_player_number: int = Field(default=-1)

    group: "Group" = lazy_relationship(back_populates="games")

    munchkins: list["Munchkin"] = lazy_relationship(back_populates="game")
    combats: list["Combat"] = lazy_relationship(back_populates="game")


class Munchkin(CustomSQLModel, table=True):
    """Информация о манчкине"""

    __table_args__ = (UniqueConstraint("user_id", "game_id"), )

    id: int | None = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="tg_user.tg_id")
    game_id: int = Field(foreign_key="game.id")

    gender: Gender = Field(default=Gender.MALE, sa_type=ENUM(Gender)) # type: ignore[call-overload]
    number: int = Field(default=-1, sa_type=SmallInteger)
    level: int = Field(default=1, sa_type=SmallInteger)
    strength: int = Field(default=1, sa_type=SmallInteger)
    luck: int = Field(default=0, sa_type=SmallInteger)
    runaway_bonus: int = Field(default=0, sa_type=SmallInteger)

    user: "User" = lazy_relationship(back_populates="munchkins")
    game: Game = lazy_relationship(back_populates="munchkins")

    turns: list["Turn"] = lazy_relationship(back_populates="munchkin")
    combats: list["Combat"] = lazy_relationship(back_populates="munchkins",
                                                link_model=MunchkinCombat)
    cards: list["GameCard"] = lazy_relationship(back_populates="munchkins",
                                                link_model=MunchkinCard)
    items: list["GameItem"] = lazy_relationship(back_populates="munchkins",
                                                link_model=MunchkinItem)


class Turn(CustomSQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    munchkin_id: int = Field(foreign_key="munchkin.id")
    turn_type: TurnType = Field(sa_type=ENUM(TurnType)) # type: ignore[call-overload]

    munchkin: Munchkin = lazy_relationship(back_populates="turns")


class Combat(CustomSQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    game_id: int = Field(foreign_key="game.id")
    difference: int = Field(sa_type=SmallInteger)
    munchkin_can_join: bool
    monster_can_join: bool
    is_active: bool
    is_runaway: bool

    game: Game = lazy_relationship(back_populates="combats")

    munchkins: list[Munchkin] = lazy_relationship(back_populates="combats",
                                                  link_model=MunchkinCombat)
