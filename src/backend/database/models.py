"""
Модели для базы данных, связанной с процессом игры.
Все классы, представленные здесь, являются либо таблицами,
либо "абстрактными" классами
"""

from enum import Enum
from typing import Optional

from sqlmodel import Field, Relationship, UniqueConstraint
from sqlalchemy import Column, BigInteger, SmallInteger, Text
from sqlalchemy.dialects.postgresql import ENUM
from pydantic import field_validator, ValidationError

from backend.database import CustomSQLModel

'''
Технические функции/классы
'''
def LazyRelationship(*args, **kwargs):
    return Relationship(*args,
                        sa_relationship_kwargs={'lazy': 'selectin'},
                        **kwargs)


'''
Enum'ы
'''

class Gender(str, Enum):
    MALE = 'male'
    FEMALE = 'female'


class TurnType(str, Enum):
    KICK_DOOR = 'kick_door'
    LOOK_TROUBLE = 'look_trouble'
    LOOT_ROOM = 'loot_room'
    CHARITY = 'charity'
    COMBAT = 'combat'


class CardType(str, Enum):
    DOOR = 'door'
    TREASURE = 'treasure'


class ItemType(str, Enum):
    HEADGEAR = 'головняк'
    ARMOR = 'броник'
    FOOTGEAR = 'обувка'
    HAND = 'рука'


class ItemProperty(str, Enum):
    FLAME = 'огненная'
    WOODEN = 'древесная'
    STICK = 'палка/жезл/посох'


class SourceType(str, Enum):
    DOOR_DECK = 'колода дверей'
    TREASURE_DECK = 'колода сокровищ'
    DOOR_DISCARD = 'сброс дверей'
    TREASURE_DISCARD = 'сброс сокровищ'
    PLAYER = 'игрок'


class MonsterType(str, Enum):
    UNDEAD = 'undead'


'''
Таблицы многие ко многим
'''

class MunchkinCombat(CustomSQLModel, table=True):
    munchkin_id: int | None = Field(default=None,
                                    primary_key=True,
                                    foreign_key="munchkin.id")
    combat_id: int | None = Field(default=None,
                                  primary_key=True,
                                  foreign_key="combat.id")
    modifier: int = Field(sa_column=Column(SmallInteger(), nullable=False))
    runaway_bonus: int = Field(sa_column=Column(SmallInteger(), nullable=False))
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


'''
Обычные таблицы
'''
class UserBase(CustomSQLModel):
    tg_id: int


class User(UserBase, table=True):
    """Пользователь"""

    __tablename__ = 'tg_user'

    tg_id: int = Field(sa_column=Column(
        BigInteger(), primary_key=True, autoincrement=False, nullable=False))
    user_name: str = Field(unique=True, max_length=32)
    full_name: str = Field(unique=True, max_length=128)

    munchkins: list["Munchkin"] = LazyRelationship(back_populates="user")


class GroupBase(CustomSQLModel):
    tg_id: int


class Group(GroupBase, table=True):
    """Телеграм группа"""

    __tablename__ = 'tg_group'

    tg_id: int = Field(sa_column=Column(
        BigInteger(), primary_key=True, autoincrement=False, nullable=False))
    name: str = Field(unique=True, max_length=32)

    games: list["Game"] = LazyRelationship(back_populates="group")


class Game(CustomSQLModel, table=True):
    """Информация об игровой партии"""

    id: int | None = Field(default=None, primary_key=True)
    group_id: int = Field(foreign_key="tg_group.tg_id")
    on_going: bool = Field(default=False)
    current_player_number: int = Field(default=-1)

    group: Group = Relationship(back_populates="games")

    munchkins: list["Munchkin"] = LazyRelationship(back_populates="game")
    combats: list["Combat"] = LazyRelationship(back_populates="game")


class Munchkin(CustomSQLModel, table=True):
    """Информация о манчкине"""

    __table_args__ = (UniqueConstraint("user_id", "game_id"), )

    id: int | None = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="tg_user.tg_id")
    game_id: int = Field(foreign_key="game.id")

    gender: Gender = Field(default=Gender.MALE,
                           sa_type=ENUM(Gender))
    number: int = Field(default=-1,
                        sa_type=SmallInteger)
    level: int = Field(default=1, sa_type=SmallInteger)
    strength: int = Field(default=1,
                          sa_type=SmallInteger)
    luck: int = Field(default=0, sa_type=SmallInteger)
    runaway_bonus: int = Field(default=0,
                               sa_type=SmallInteger)

    user: User = LazyRelationship(back_populates="munchkins")
    game: Game = LazyRelationship(back_populates="munchkins")

    turns: list["Turn"] = LazyRelationship(back_populates="munchkin")
    combats: list["Combat"] = LazyRelationship(back_populates="munchkins",
                                               link_model=MunchkinCombat)
    cards: list["GameCard"] = LazyRelationship(back_populates="munchkins",
                                               link_model=MunchkinCard)
    items: list["GameItem"] = LazyRelationship(back_populates="munchkins",
                                               link_model=MunchkinItem)


class Turn(CustomSQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    munchkin_id: int = Field(foreign_key="munchkin.id")
    turn_type: TurnType = Field(sa_type=ENUM(TurnType))

    munchkin: Munchkin = LazyRelationship(back_populates="turns")


class Combat(CustomSQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    game_id: int = Field(foreign_key="game.id")
    difference: int = Field(sa_type=SmallInteger)
    munchkin_can_join: bool
    monster_can_join: bool
    is_active: bool
    is_runaway: bool

    game: Game = LazyRelationship(back_populates="combats")

    munchkins: list[Munchkin] = LazyRelationship(back_populates="combats",
                                                 link_model=MunchkinCombat)


class CardBase(CustomSQLModel):
    name: str = Field(unique=True, max_length=64)
    image_path: str = Field(unique=True, max_length=64)
    description: str = Field(sa_type=Text, unique=True)
    card_type: CardType = Field(sa_type=ENUM(CardType))
    # action_group_id: int =


class Card(CardBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    game_cards: list["GameCard"] = LazyRelationship(back_populates="card")
    item: Optional["Item"] = LazyRelationship(back_populates="card")
    monster: Optional["Monster"] = LazyRelationship(back_populates="card")


class GameCard(CustomSQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    card_id: int = Field(foreign_key="card.id")
    source_type: SourceType = Field(sa_type=ENUM(SourceType))
    open: bool

    card: Card = LazyRelationship(back_populates="game_cards")
    munchkins: list["Munchkin"] = LazyRelationship(back_populates="cards",
                                                   link_model=MunchkinCard)
    game_item: "GameItem" = LazyRelationship(back_populates="game_card")
    

class Treasure(CardBase):
    card_type: CardType = CardType.TREASURE

    @field_validator("card_type", mode='after')
    @classmethod
    def check_treasure(cls, value: CardType) -> CardType:
        if value != CardType.TREASURE:
            raise ValueError('Попытка создать сокровище со значение card_type=door')
        return value
    

class Door(CardBase):
    card_type: CardType = CardType.DOOR

    @field_validator("card_type", mode='after')
    @classmethod
    def check_door(cls, value: CardType) -> CardType:
        if value != CardType.DOOR:
            raise ValueError('Попытка создать дверь со значение card_type=treasure')
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

    card: Card = LazyRelationship(back_populates="monster")


class ItemBase(CustomSQLModel):
    bonus: int = Field(sa_type=SmallInteger)
    runaway_bonus: int | None = Field(default=None,
                                      sa_type=SmallInteger)
    one_shot: bool
    is_big: bool
    is_hireling: bool
    price: int | None = Field(default=None, sa_type=SmallInteger)


    item_type: ItemType | None = Field(default=None,
                                       sa_type=ENUM(ItemType))
    hand_count: int | None = Field(default=None, sa_type=SmallInteger)
    item_property: ItemProperty | None = Field(default=None,
                                               sa_type=ENUM(ItemProperty))


class ItemCreate(Treasure, ItemBase):
    pass


class Item(ItemBase, table=True):
    card_id: int = Field(foreign_key="card.id", primary_key=True)
    
    card: Card = LazyRelationship(back_populates="item")
    game_items: list["GameItem"] = LazyRelationship(back_populates="original_item")
    

class GameItem(ItemBase, table=True):
    game_card_id: int = Field(foreign_key="gamecard.id", primary_key=True)
    original_item_id: int = Field(foreign_key="item.card_id")

    game_card: GameCard = LazyRelationship(back_populates="game_item")
    original_item: Item = LazyRelationship(back_populates="game_items")
    munchkins: list[Munchkin] = LazyRelationship(back_populates="items",
                                                 link_model=MunchkinItem)


# class Stats(CustomSQLModel, table = True):
#     pass

# class StatsType(CustomSQLModel, table = True):
#     pass

# class MunchkinStats(CustomSQLModel, table = True):
#     pass

# class MunchkinItem(CustomSQLModel, table = True):
#     pass

# class Munchkin(CustomSQLModel, table = True):
#     pass

# class MunchkinCombat(CustomSQLModel, table = True):
#     pass

# class MonsterCombat(CustomSQLModel, table = True):
#     pass

# class Combat(CustomSQLModel, table = True):
#     pass

# class MunchkinCards(CustomSQLModel, table = True):
#     pass

# class Monster(CustomSQLModel, table = True):
#     pass

# class UndeadType(CustomSQLModel, table = True):
#     pass
