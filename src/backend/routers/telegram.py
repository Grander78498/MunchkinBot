"""Получение информации о пользователях."""

from typing import Any

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError

from backend.database import AsyncGameSession
from backend.database.responses import SuccessfulResponse
from backend.database.users import User
from backend.utils.db_functions import get_user

router = APIRouter(
    prefix="/telegram",
    tags=["Telegram"],
)


@router.post("/user", response_model=SuccessfulResponse)
async def save_user(user: User, session: AsyncGameSession) -> Any:
    """Сохранение информации о пользователе."""
    try:
        async with session.begin():
            session.add(user)
    except IntegrityError as e:
        raise HTTPException(
            status_code=404,
            detail="Такой пользователь уже существует",
        ) from e

    return {"msg": "All good"}


@router.get("/user")
async def get_user_info(session: AsyncGameSession, user_id: int | None = None, user_name: str | None = None) -> User:
    """Получение информации о пользователе."""
    async with session.begin():
        user = await get_user(session, user_id=user_id, user_name=user_name)
        return user
