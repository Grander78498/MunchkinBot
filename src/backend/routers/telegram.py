"""Получение информации о пользователях."""

from typing import Any

from fastapi import APIRouter
from backend.database import AsyncGameSession
from backend.utils.db_functions import get_user
from backend.database.users import User
from backend.database.responses import SuccessfulResponse

router = APIRouter(
    prefix="/telegram",
    tags=["Telegram"],
)


@router.post("/user", response_model=SuccessfulResponse)
async def save_user(user: User, session: AsyncGameSession) -> Any:
    """Сохранение информации о пользователе."""
    async with session.begin():
        session.add(user)

    return {"msg": "All good"}


@router.get("/user/{user_id}")
async def get_user_info(user_id: int, session: AsyncGameSession) -> User:
    """Получение информации о пользователе."""
    async with session.begin():
        user = await get_user(user_id, session)
        return user
