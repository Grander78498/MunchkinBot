"""Таблицы для связей многие-ко-многим."""

from sqlmodel import Field
from sqlalchemy import SmallInteger
from backend.database import CustomSQLModel


class MunchkinCombat(CustomSQLModel, table=True):
    """Связь между манчкином и боем."""

    munchkin_id: int | None = Field(
        default=None, primary_key=True, foreign_key="munchkin.id"
    )
    combat_id: int | None = Field(
        default=None, primary_key=True, foreign_key="combat.id"
    )
    modifier: int = Field(sa_type=SmallInteger)
    runaway_bonus: int = Field(sa_type=SmallInteger)
    is_helping: bool


class MunchkinCard(CustomSQLModel, table=True):
    """Связь между манчкином и карточками."""

    munchkin_id: int | None = Field(
        default=None, primary_key=True, foreign_key="munchkin.id"
    )
    card_id: int | None = Field(
        default=None, primary_key=True, foreign_key="gamecard.id"
    )
    in_game: bool


class MunchkinItem(CustomSQLModel, table=True):
    """Связь между манчкином и шмотками."""

    munchkin_id: int | None = Field(
        default=None, primary_key=True, foreign_key="munchkin.id"
    )
    item_id: int | None = Field(
        default=None, primary_key=True, foreign_key="gameitem.game_card_id"
    )
    in_game: bool


class MonsterCombat(CustomSQLModel, table=True):
    """Связь между монстром и боем."""

    monster_id: int | None = Field(
        default=None, primary_key=True, foreign_key="monster.card_id"
    )
    combat_id: int | None = Field(
        default=None, primary_key=True, foreign_key="combat.id"
    )
    modifier: int = Field(default=0, sa_type=SmallInteger)
    treasure_count: int = Field(default=1, sa_type=SmallInteger)
    reward_level_count: int = Field(default=1, sa_type=SmallInteger)


class MunchkinStats(CustomSQLModel, table=True):
    """Связь между манчкином и характеристиками."""

    munchkin_id: int | None = Field(
        default=None, primary_key=True, foreign_key="munchkin.id"
    )
    stats_id: int | None = Field(
        default=None, primary_key=True, foreign_key="stats.card_id"
    )


class CardAction(CustomSQLModel, table=True):
    """Связь между карточками и действиями."""

    action_id: int | None = Field(
        default=None, primary_key=True, foreign_key="action.id"
    )
    card_id: int | None = Field(
        default=None, primary_key=True, foreign_key="card.id"
    )


class ActionCondition(CustomSQLModel, table=True):
    """Связь между действиями и условиями."""

    action_id: int | None = Field(
        default=None, primary_key=True, foreign_key="action.id"
    )
    condition_id: int | None = Field(
        default=None, primary_key=True, foreign_key="condition.id"
    )


class CardsTransferCondition(CustomSQLModel, table=True):
    """Связь между условиями и действиями по получению/передачи карточек."""

    cards_transfer_id: int | None = Field(
        default=None, primary_key=True, foreign_key="cardstransfer.action_id"
    )
    condition_id: int | None = Field(
        default=None, primary_key=True, foreign_key="condition.id"
    )


class ItemCondition(CustomSQLModel, table=True):
    """Связь между шмотками и условиями."""

    item_id: int | None = Field(
        default=None, primary_key=True, foreign_key="item.card_id"
    )
    condition_id: int | None = Field(
        default=None, primary_key=True, foreign_key="condition.id"
    )


class ActionMunchkin(CustomSQLModel, table=True):
    """Связь между манчкином и действием."""

    action_id: int | None = Field(
        default=None, primary_key=True, foreign_key="action.id"
    )
    munchkin_id: int | None = Field(
        default=None, primary_key=True, foreign_key="munchkin.id"
    )
    is_initiator: bool


class ActionMonster(CustomSQLModel, table=True):
    """Связь между монстром и действием."""

    action_id: int | None = Field(
        default=None, primary_key=True, foreign_key="action.id"
    )
    monster_id: int | None = Field(
        default=None, primary_key=True, foreign_key="monster.card_id"
    )
