"""Получение информации о действиях."""

from fastapi import APIRouter
from backend.database import AsyncGameSession
from backend.utils.db_functions import get_condition
from backend.database.conditions import Condition

router = APIRouter(
    prefix="/action",
    tags=["Actions"],
)


@router.get("/{condition_id}")
async def get_condition_info(
    condition_id: int, session: AsyncGameSession
) -> Condition:
    """Получение информации о пользователе."""
    async with session.begin():
        condition = await get_condition(condition_id, session)
        return condition
