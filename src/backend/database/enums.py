from enum import Enum


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