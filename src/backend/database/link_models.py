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


class MonsterCombat(CustomSQLModel, table = True):
    monster_id: int | None = Field(default=None,
                                   primary_key=True,
                                   foreign_key="monster.card_id")
    combat_id: int | None = Field(default=None,
                            primary_key=True,
                            foreign_key="combat.id")
    modifier: int = Field(default=0, sa_type=SmallInteger)
    treasure_count: int = Field(default=1, sa_type=SmallInteger)
    reward_level_count: int = Field(default=1, sa_type=SmallInteger)


class MunchkinStats(CustomSQLModel, table = True):
    munchkin_id: int | None = Field(default=None,
                                   primary_key=True,
                                   foreign_key="munchkin.id")
    stats_id: int | None = Field(default=None,
                            primary_key=True,
                            foreign_key="stats.card_id")
    

class CardAction(CustomSQLModel, table=True):
    action_id: int | None = Field(default=None,
                                   primary_key=True,
                                   foreign_key="action.id")
    card_id: int | None = Field(default=None,
                            primary_key=True,
                            foreign_key="card.id")
    

class ActionCondition(CustomSQLModel, table = True):
    action_id: int | None = Field(default=None,
                                   primary_key=True,
                                   foreign_key="action.id")
    condition_id: int | None = Field(default=None,
                            primary_key=True,
                            foreign_key="condition.id")
    

class CardsTransferCondition(CustomSQLModel, table = True):
    cards_transfer_id: int | None = Field(default=None,
                                   primary_key=True,
                                   foreign_key="cardstransfer.action_id")
    condition_id: int | None = Field(default=None,
                            primary_key=True,
                            foreign_key="condition.id")
    

class ItemCondition(CustomSQLModel, table = True):
    item_id: int | None = Field(default=None,
                                   primary_key=True,
                                   foreign_key="item.card_id")
    condition_id: int | None = Field(default=None,
                            primary_key=True,
                            foreign_key="condition.id")
    

class ActionMunchkin(CustomSQLModel, table = True):
    action_id: int | None = Field(default=None,
                                   primary_key=True,
                                   foreign_key="action.id")
    munchkin_id: int | None = Field(default=None,
                            primary_key=True,
                            foreign_key="munchkin.id")
    is_initiator: bool


class ActionMonster(CustomSQLModel, table = True):
    action_id: int | None = Field(default=None,
                                   primary_key=True,
                                   foreign_key="action.id")
    monster_id: int | None = Field(default=None,
                            primary_key=True,
                            foreign_key="monster.card_id")