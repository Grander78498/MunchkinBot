"""
Таблицы для хранения различных условий.
"""

from typing import TYPE_CHECKING

from sqlmodel import Field
from sqlalchemy.dialects.postgresql import ENUM

from backend.database import CustomSQLModel, lazy_relationship
from backend.database.enums import EqualType
from backend.database.link_models import (
    ItemCondition,
    ActionCondition,
    CardsTransferCondition,
)

if TYPE_CHECKING:
    from backend.database.actions import Action, CardsTransfer
    from backend.database.cards import Item


class Condition(CustomSQLModel, table=True):
    """Условие, при котором выполняется какое-либо действие."""

    id: int | None = Field(default=None, primary_key=True)
    value_id: int = Field(foreign_key="possibleconditionvalue.id")
    equal_type: EqualType = Field(
        sa_type=ENUM(EqualType)
    )  # type: ignore [call-overload]

    value: "PossibleConditionValue" = lazy_relationship(back_populates="conditions")
    actions: list["Action"] = lazy_relationship(
        back_populates="conditions", link_model=ActionCondition
    )
    items: list["Item"] = lazy_relationship(
        back_populates="conditions", link_model=ItemCondition
    )
    cards_transfers: list["CardsTransfer"] = lazy_relationship(
        back_populates="conditions", link_model=CardsTransferCondition
    )


class PossibleConditionValue(CustomSQLModel, table=True):
    """Возможное значение, фигурирующее в условии"""

    id: int | None = Field(default=None, primary_key=True)
    field_id: int = Field(foreign_key="possibleconditionfield.id")
    name: str = Field(max_length=64)

    field: "PossibleConditionField" = lazy_relationship(back_populates="values")
    conditions: list[Condition] = lazy_relationship(back_populates="value")


class PossibleConditionField(CustomSQLModel, table=True):
    """Возможное поле, значение которого проверяется в условии"""

    id: int | None = Field(default=None, primary_key=True)
    type_id: int = Field(foreign_key="possibleconditiontype.id")
    name: str = Field(max_length=64)

    type: "PossibleConditionType" = lazy_relationship(back_populates="fields")
    values: list[PossibleConditionValue] = lazy_relationship(back_populates="field")


class PossibleConditionType(CustomSQLModel, table=True):
    """Возможный тип объекта, который проверяется в условии"""

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=64)

    fields: list[PossibleConditionField] = lazy_relationship(back_populates="type")
