"""
Модели для базы данных, связанной с процессом игры.
Все классы, представленные здесь, являются либо таблицами,
либо "абстрактными" классами
"""

from enum import Enum

from sqlmodel import Field, Relationship, UniqueConstraint
from sqlalchemy import Column, BigInteger, SmallInteger, Text
from sqlalchemy.dialects.postgresql import ENUM

from backend.database import CustomSQLModel


def LazyRelationship(*args, **kwargs):
    return Relationship(*args,
                        sa_relationship_kwargs={'lazy': 'selectin'},
                        **kwargs)


class NotNullableColumn(Column):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, nullable=False, **kwargs)


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
    ONE_HAND = 'в 1 руку'
    TWO_HAND = 'в 2 руки'
    THREE_HAND = 'в 3 руки'
    MINUS_HAND = '-1 рука'


class ItemProperty(str, Enum):
    FLAME = 'огненная'
    WOODEN = 'древесная'
    STICK = 'палка/жезл/посох'


class MunchkinCombat(CustomSQLModel, table=True):
    munchkin_id: int | None = Field(default=None,
                                    primary_key=True,
                                    foreign_key="munchkin.id")
    combat_id: int | None = Field(default=None,
                                  primary_key=True,
                                  foreign_key="combat.id")
    modifier: int = Field(sa_column=NotNullableColumn(SmallInteger()))
    runaway_bonus: int = Field(sa_column=NotNullableColumn(SmallInteger()))
    is_helping: bool


class UserBase(CustomSQLModel):
    tg_id: int


class User(UserBase, table=True):
    """Пользователь"""

    __tablename__ = 'tg_user'

    tg_id: int = Field(sa_column=NotNullableColumn(
        BigInteger(), primary_key=True, autoincrement=False))
    user_name: str = Field(unique=True, max_length=32)
    full_name: str = Field(unique=True, max_length=128)

    munchkins: list["Munchkin"] = LazyRelationship(back_populates="user")


class GroupBase(CustomSQLModel):
    tg_id: int


class Group(GroupBase, table=True):
    """Телеграм группа"""

    __tablename__ = 'tg_group'

    tg_id: int = Field(sa_column=NotNullableColumn(
        BigInteger(), primary_key=True, autoincrement=False))
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
                           sa_column=NotNullableColumn(ENUM(Gender)))
    number: int = Field(default=-1,
                        sa_column=NotNullableColumn(SmallInteger()))
    level: int = Field(default=1, sa_column=NotNullableColumn(SmallInteger()))
    strength: int = Field(default=1,
                          sa_column=NotNullableColumn(SmallInteger()))
    luck: int = Field(default=0, sa_column=NotNullableColumn(SmallInteger()))
    runaway_bonus: int = Field(default=0,
                               sa_column=NotNullableColumn(SmallInteger()))

    user: User = LazyRelationship(back_populates="munchkins")
    game: Game = LazyRelationship(back_populates="munchkins")

    turns: list["Turn"] = LazyRelationship(back_populates="munchkin")
    combats: list["Combat"] = LazyRelationship(back_populates="munchkins",
                                               link_model=MunchkinCombat)


class Turn(CustomSQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    munchkin_id: int = Field(foreign_key="munchkin.id")
    turn_type: TurnType = Field(sa_column=NotNullableColumn(ENUM(TurnType)))

    munchkin: Munchkin = LazyRelationship(back_populates="turns")


class Combat(CustomSQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    game_id: int = Field(foreign_key="game.id")
    difference: int = Field(sa_column=NotNullableColumn(SmallInteger()))
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
    description: str
    # action_group_id: int =
    card_type: CardType = Field(sa_column=NotNullableColumn(ENUM(CardType)))


class Card(CardBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    description: str = Field(sa_column=NotNullableColumn(Text(), unique=True))


class Treasure(CardBase):
    card_type: CardType = CardType.TREASURE


class ItemBase(Treasure):
    bonus: int
    runaway_bonus: int | None
    one_shot: bool
    is_big: bool
    is_hireling: bool
    price: int | None
    item_type: ItemType | None
    item_property: ItemProperty | None


class Item(ItemBase, table=True):
    card_id: int = Field(foreign_key="card.id", primary_key=True)
    description: str = Field(sa_column=NotNullableColumn(Text(), unique=True))

    bonus: int = Field(sa_column=NotNullableColumn(SmallInteger()))
    runway_bonus: int | None = Field(default=None,
                                     sa_column=Column(SmallInteger()))
    price: int | None = Field(default=None, sa_column=Column(SmallInteger()))

    item_type: ItemType | None = Field(default=None,
                                       sa_column=Column(ENUM(ItemType)))
    item_property: ItemProperty | None = Field(default=None,
                                               sa_column=Column(
                                                   ENUM(ItemProperty)))


'''
class CardType(str, Enum):
    DOOR = "door"
    TREASURE = "treasure"

class CardBase(CustomSQLModel):
    name: str = Field(unique=True, max_length=64)
    description: str = Field(unique=True)
    image_path: str = Field(unique=True, max_length=64)
    card_type: CardType = Field(sa_column=Column(SQLEnum(CardType)))

class Card(CardBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class TreasureBase(CardBase):
    card_type: CardType = CardType.TREASURE

class Treasure(TreasureBase, Card, table=True):
    id: int = Field(foreign_key="card.id", primary_key=True)

class ItemBase(TreasureBase):
    bonus: int

class Item(ItemBase, Treasure, table=True):
    id: int = Field(foreign_key="treasure.id", primary_key=True)
'''

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
