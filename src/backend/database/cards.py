"""
Таблицы для обращения к карточкам, включая подвиды.
"""

from typing import TYPE_CHECKING, Optional

from pydantic import field_validator
from sqlmodel import Field
from sqlalchemy import SmallInteger, Text
from sqlalchemy.dialects.postgresql import ENUM

from backend.database import CustomSQLModel, lazy_relationship
from backend.database.link_models import (
    MunchkinCard,
    MunchkinItem,
    MonsterCombat,
    MunchkinStats,
    CardAction,
    ItemCondition,
    ActionMonster,
)
from backend.database.enums import CardType, SourceType

if TYPE_CHECKING:
    from backend.database.game import Munchkin, Combat
    from backend.database.actions import Action
    from backend.database.conditions import Condition


class ItemType(CustomSQLModel, table=True):
    """
    Тип шмотки - головняк, броник и т.п.
    """

    id: int | None = Field(default=None, primary_key=True)
    item_type: str = Field(max_length=64)

    items: list["Item"] = lazy_relationship(back_populates="item_type")


class ItemProperty(CustomSQLModel, table=True):
    """
    Свойство шмотки - обладает огненной атакой, является палкой или т.п.
    """

    id: int | None = Field(default=None, primary_key=True)
    item_property: str = Field(max_length=64)

    items: list["Item"] = lazy_relationship(back_populates="item_property")


class MonsterType(CustomSQLModel, table=True):
    """
    Тип монстра - андед, дракон и т.п.
    """

    id: int | None = Field(default=None, primary_key=True)
    monster_type: str = Field(max_length=64)

    monsters: list["Monster"] = lazy_relationship(back_populates="monster_type")


class StatsType(CustomSQLModel, table=True):
    """
    Название характеристики манчикна - класс, раса, стиль и т.п.
    """

    id: int | None = Field(default=None, primary_key=True)
    stats_type: str = Field(max_length=64)

    stats_cards: list["Stats"] = lazy_relationship(back_populates="stats_type")


class CardBase(CustomSQLModel):
    """
    Базовый класс для карточки, нужен для реализации наследования.
    """

    name: str = Field(unique=True, max_length=64)
    image_path: str = Field(unique=True, max_length=64)
    description: str = Field(sa_type=Text, unique=True)
    card_type: CardType = Field(sa_type=ENUM(CardType))  # type: ignore[call-overload]


class Card(CardBase, table=True):
    """
    Таблица карточки.
    """

    id: int | None = Field(default=None, primary_key=True)

    game_cards: list["GameCard"] = lazy_relationship(back_populates="card")
    item: Optional["Item"] = lazy_relationship(back_populates="card")
    monster: Optional["Monster"] = lazy_relationship(back_populates="card")

    actions: list["Action"] = lazy_relationship(
        back_populates="cards", link_model=CardAction
    )


class GameCard(CustomSQLModel, table=True):
    """
    Карточка, которая находится в игре.
    """

    id: int | None = Field(default=None, primary_key=True)
    card_id: int = Field(foreign_key="card.id")
    source_type: SourceType = Field(
        sa_type=ENUM(SourceType)
    )  # type: ignore[call-overload]
    open: bool

    card: Card = lazy_relationship(back_populates="game_cards")
    munchkins: list["Munchkin"] = lazy_relationship(
        back_populates="cards", link_model=MunchkinCard
    )
    game_item: "GameItem" = lazy_relationship(back_populates="game_card")


class Treasure(CardBase):
    """Родительский класс для карт, являющихся сокровищами."""

    card_type: CardType = CardType.TREASURE

    @field_validator("card_type", mode="after")
    @classmethod
    def check_treasure(cls, value: CardType) -> CardType:
        """
        Проверка, что не попытались создать дверь под видом сокровища.
        """
        if value != CardType.TREASURE:
            raise ValueError("Попытка создать сокровище со значение card_type=door")
        return value


class Door(CardBase):
    """Родительский класс для карт, являющихся дверьми."""

    card_type: CardType = CardType.DOOR

    @field_validator("card_type", mode="after")
    @classmethod
    def check_door(cls, value: CardType) -> CardType:
        """
        Проверка, что не попытались создать сокровище под видом двери.
        """
        if value != CardType.DOOR:
            raise ValueError("Попытка создать дверь со значение card_type=treasure")
        return value


class MonsterBase(CustomSQLModel):
    """
    Базовый класс для монстра.
    """

    level: int = Field(default=1, sa_type=SmallInteger)
    strength: int = Field(default=1, sa_type=SmallInteger)
    treasure_count: int
    reward_level_count: int
    monster_type_id: int | None = Field(default=None, foreign_key="monstertype.id")


class MonsterCreate(Door, MonsterBase):
    """Создание монстра."""


class Monster(MonsterBase, table=True):
    """
    Таблица монстра.
    """

    card_id: int = Field(foreign_key="card.id", primary_key=True)

    card: Card = lazy_relationship(back_populates="monster")
    combats: list["Combat"] = lazy_relationship(
        back_populates="monsters", link_model=MonsterCombat
    )
    monster_type: MonsterType | None = lazy_relationship(back_populates="monsters")
    actions: list["Action"] = lazy_relationship(
        back_populates="monsters", link_model=ActionMonster
    )


class StatsBase(CustomSQLModel):
    """Базовый класс для характеристик манчкина."""

    stats_type_id: int = Field(foreign_key="statstype.id")


class StatsCreate(Door, StatsBase):
    """Создание характеристик манчкина."""


class Stats(MonsterBase, table=True):
    """Таблица для характеристик манчкина."""

    card_id: int = Field(foreign_key="card.id", primary_key=True)

    card: Card = lazy_relationship(back_populates="monster")
    munchkins: list["Munchkin"] = lazy_relationship(
        back_populates="stats", link_model=MunchkinStats
    )
    stats_type: StatsType = lazy_relationship(back_populates="stats_cards")


class ItemBase(CustomSQLModel):
    """Базовый класс для шмоток."""

    bonus: int = Field(sa_type=SmallInteger)
    runaway_bonus: int | None = Field(default=None, sa_type=SmallInteger)
    one_shot: bool
    is_big: bool
    is_hireling: bool
    price: int | None = Field(default=None, sa_type=SmallInteger)
    item_type_id: int | None = Field(default=None, foreign_key="itemtype.id")
    item_property_id: int | None = Field(default=None, foreign_key="itemproperty.id")

    hand_count: int | None = Field(default=None, sa_type=SmallInteger)


class ItemCreate(Treasure, ItemBase):
    """Создание шмотки."""


class Item(ItemBase, table=True):
    """Таблица шмотки."""

    card_id: int = Field(foreign_key="card.id", primary_key=True)

    card: Card = lazy_relationship(back_populates="item")
    game_items: list["GameItem"] = lazy_relationship(back_populates="original_item")
    item_type: ItemType | None = lazy_relationship(back_populates="items")
    item_property: ItemProperty | None = lazy_relationship(back_populates="items")

    conditions: list["Condition"] = lazy_relationship(
        back_populates="items", link_model=ItemCondition
    )


class GameItem(ItemBase, table=True):
    """Шмотка в игре."""

    game_card_id: int = Field(foreign_key="gamecard.id", primary_key=True)
    original_item_id: int = Field(foreign_key="item.card_id")

    game_card: GameCard = lazy_relationship(back_populates="game_item")
    original_item: Item = lazy_relationship(back_populates="game_items")
    munchkins: list["Munchkin"] = lazy_relationship(
        back_populates="items", link_model=MunchkinItem
    )
