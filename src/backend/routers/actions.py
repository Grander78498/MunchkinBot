"""Получение информации о действиях."""

from fastapi import APIRouter
from backend.database import AsyncGameSession
from backend.utils.db_functions import get_action
from backend.database.actions import Action

router = APIRouter(
    prefix="/action",
    tags=["Actions"],
)



@router.get("/{action_id}")
async def get_action_info(action_id: int, session: AsyncGameSession) -> Action:
    """Получение информации о пользователе."""
    async with session.begin():
        action = await get_action(action_id, session)
        return action