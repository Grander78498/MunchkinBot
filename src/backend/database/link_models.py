from sqlmodel import Field
from sqlalchemy import Column, SmallInteger
from backend.database import CustomSQLModel


class MunchkinCombat(CustomSQLModel, table=True):
    munchkin_id: int | None = Field(default=None,
                                    primary_key=True,
                                    foreign_key="munchkin.id")
    combat_id: int | None = Field(default=None,
                                  primary_key=True,
                                  foreign_key="combat.id")
    modifier: int = Field(sa_type=SmallInteger)
    runaway_bonus: int = Field(sa_type=SmallInteger)
    is_helping: bool


class MunchkinCard(CustomSQLModel, table=True):
    munchkin_id: int | None = Field(default=None,
                                    primary_key=True,
                                    foreign_key="munchkin.id")
    card_id: int | None = Field(default=None,
                                primary_key=True,
                                foreign_key="gamecard.id")
    in_game: bool


class MunchkinItem(CustomSQLModel, table=True):
    munchkin_id: int | None = Field(default=None,
                                    primary_key=True,
                                    foreign_key="munchkin.id")
    item_id: int | None = Field(default=None,
                                primary_key=True,
                                foreign_key="gameitem.game_card_id")
    in_game: bool
