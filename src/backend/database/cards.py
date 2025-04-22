from typing import TYPE_CHECKING, Optional

from pydantic import field_validator
from sqlmodel import Field
from sqlalchemy import SmallInteger, Text
from sqlalchemy.dialects.postgresql import ENUM

from backend.database import CustomSQLModel, lazy_relationship
from backend.database.link_models import MunchkinCard, MunchkinItem
from backend.database.enums import CardType, SourceType, MonsterType, ItemProperty, ItemType

if TYPE_CHECKING:
    from backend.database.game import Munchkin


class CardBase(CustomSQLModel):
    name: str = Field(unique=True, max_length=64)
    image_path: str = Field(unique=True, max_length=64)
    description: str = Field(sa_type=Text, unique=True)
    card_type: CardType = Field(sa_type=ENUM(CardType))
    # action_group_id: int =


class Card(CardBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    game_cards: list["GameCard"] = lazy_relationship(back_populates="card")
    item: Optional["Item"] = lazy_relationship(back_populates="card")
    monster: Optional["Monster"] = lazy_relationship(back_populates="card")


class GameCard(CustomSQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    card_id: int = Field(foreign_key="card.id")
    source_type: SourceType = Field(sa_type=ENUM(SourceType))
    open: bool

    card: Card = lazy_relationship(back_populates="game_cards")
    munchkins: list["Munchkin"] = lazy_relationship(back_populates="cards",
                                                    link_model=MunchkinCard)
    game_item: "GameItem" = lazy_relationship(back_populates="game_card")


class Treasure(CardBase):
    card_type: CardType = CardType.TREASURE

    @field_validator("card_type", mode='after')
    @classmethod
    def check_treasure(cls, value: CardType) -> CardType:
        if value != CardType.TREASURE:
            raise ValueError(
                'Попытка создать сокровище со значение card_type=door')
        return value


class Door(CardBase):
    card_type: CardType = CardType.DOOR

    @field_validator("card_type", mode='after')
    @classmethod
    def check_door(cls, value: CardType) -> CardType:
        if value != CardType.DOOR:
            raise ValueError(
                'Попытка создать дверь со значение card_type=treasure')
        return value


class MonsterBase(CustomSQLModel):
    level: int = Field(default=1, sa_type=SmallInteger)
    strength: int = Field(default=1, sa_type=SmallInteger)
    treasure_count: int
    reward_level_count: int
    monster_type: MonsterType | None = Field(sa_type=ENUM(MonsterType))


class MonsterCreate(Door, MonsterBase):
    pass


class Monster(MonsterBase, table=True):
    card_id: int = Field(foreign_key="card.id", primary_key=True)

    card: Card = lazy_relationship(back_populates="monster")


class ItemBase(CustomSQLModel):
    bonus: int = Field(sa_type=SmallInteger)
    runaway_bonus: int | None = Field(default=None, sa_type=SmallInteger)
    one_shot: bool
    is_big: bool
    is_hireling: bool
    price: int | None = Field(default=None, sa_type=SmallInteger)

    item_type: ItemType | None = Field(default=None, sa_type=ENUM(ItemType))
    hand_count: int | None = Field(default=None, sa_type=SmallInteger)
    item_property: ItemProperty | None = Field(default=None,
                                               sa_type=ENUM(ItemProperty))


class ItemCreate(Treasure, ItemBase):
    pass


class Item(ItemBase, table=True):
    card_id: int = Field(foreign_key="card.id", primary_key=True)

    card: Card = lazy_relationship(back_populates="item")
    game_items: list["GameItem"] = lazy_relationship(
        back_populates="original_item")


class GameItem(ItemBase, table=True):
    game_card_id: int = Field(foreign_key="gamecard.id", primary_key=True)
    original_item_id: int = Field(foreign_key="item.card_id")

    game_card: GameCard = lazy_relationship(back_populates="game_item")
    original_item: Item = lazy_relationship(back_populates="game_items")
    munchkins: list["Munchkin"] = lazy_relationship(back_populates="items",
                                                    link_model=MunchkinItem)
