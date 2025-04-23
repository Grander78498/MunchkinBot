from typing import TYPE_CHECKING, Optional

from sqlmodel import Field
from sqlalchemy import SmallInteger, Text
from sqlalchemy.dialects.postgresql import ENUM

from backend.database import CustomSQLModel, lazy_relationship
from backend.database.link_models import CardAction, ActionCondition, CardsTransferCondition, ActionMunchkin, ActionMonster

if TYPE_CHECKING:
    from backend.database.game import Munchkin
    from backend.database.conditions import Condition
    from backend.database.cards import Card, Monster


class ActionBase(CustomSQLModel):
    description: str = Field(sa_type=Text)
    optional: bool
    # count: int
    has_death: bool


class Action(ActionBase, table = True):
    id: int | None = Field(default=None, primary_key=True)
    
    stats_change: Optional["StatsChange"] = lazy_relationship(back_populates="action")
    creature_update: Optional["CreatureUpdate"] = lazy_relationship(back_populates="action")
    creature_update: Optional["CardsTransfer"] = lazy_relationship(back_populates="action")

    conditions: list["Condition"] = lazy_relationship(back_populates="actions", link_model=ActionCondition)
    cards: list["Card"] = lazy_relationship(back_populates="actions", link_model=CardAction)
    munchkins: list["Munchkin"] = lazy_relationship(back_populates="actions", link_model=ActionMunchkin)
    monsters: list["Monster"] = lazy_relationship(back_populates="actions", link_model=ActionMonster)


class StatsChangeBase(CustomSQLModel):
    amount: int = Field(default=1, sa_type=SmallInteger)
    positive: bool


class StatsChangeCreate(ActionBase, StatsChangeBase):
    pass


class StatsChange(StatsChangeBase, table = True):
    action_id: int = Field(primary_key=True, foreign_key="action.id")
    
    action: Action = lazy_relationship(back_populates="stats_change")


class CreatureUpdateBase(CustomSQLModel):
    amount: int = Field(sa_type=SmallInteger)
    to_remove: bool


class CreatureUpdateCreate(ActionBase, CreatureUpdateBase):
    pass


class CreatureUpdate(CreatureUpdateBase, table=True):
    action_id: int = Field(primary_key=True, foreign_key="action.id")
    
    action: Action = lazy_relationship(back_populates="creature_update")


class CardsTransferBase(CustomSQLModel):
    cards_count: int = Field(sa_type=SmallInteger)
    is_open: bool
    giveaway: bool


class CardsTransferCreate(ActionBase, CardsTransferBase):
    pass


class CardsTransfer(CardsTransferBase, table=True):
    action_id: int = Field(primary_key=True, foreign_key="action.id")
    
    action: Action = lazy_relationship(back_populates="cards_transfer")
    conditions: list["Condition"] = lazy_relationship(back_populates="cards_transfers", link_model=CardsTransferCondition)
