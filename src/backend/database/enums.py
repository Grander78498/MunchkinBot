from enum import Enum


class Gender(str, Enum):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'


class TurnType(str, Enum):
    KICK_DOOR = 'kick_door'
    LOOK_TROUBLE = 'look_trouble'
    LOOT_ROOM = 'loot_room'
    CHARITY = 'charity'
    COMBAT = 'combat'


class CardType(str, Enum):
    DOOR = 'door'
    TREASURE = 'treasure'


class SourceType(str, Enum):
    DOOR_DECK = 'колода дверей'
    TREASURE_DECK = 'колода сокровищ'
    DOOR_DISCARD = 'сброс дверей'
    TREASURE_DISCARD = 'сброс сокровищ'
    PLAYER = 'игрок'


class EqualType(str, Enum):
    LT = 'less than'
    LE = 'less equal'
    EQ = 'equal'
    NQ = 'not equal'
    GE = 'greater equal'
    GT = 'greater than'