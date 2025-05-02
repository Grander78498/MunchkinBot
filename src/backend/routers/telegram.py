"""
Получение информации о пользователях
"""

from typing import Any

from fastapi import APIRouter
from backend.database import AsyncGameSession
from backend.database.functions import get_user, get_group
from backend.database.users import User, Group
from backend.database.responses import SuccessfulResponse

router = APIRouter(
    prefix="/telegram",
    tags=["Telegram"],
)


@router.post("/user", response_model=SuccessfulResponse)
async def save_user(user: User, session: AsyncGameSession) -> Any:
    """Сохранение информации о пользователе"""

    async with session.begin():
        session.add(user)

    return {"msg": "All good"}


@router.post("/group", response_model=SuccessfulResponse)
async def save_group(group: Group, session: AsyncGameSession) -> Any:
    """Сохранение информации о группе"""

    async with session.begin():
        session.add(group)

    return {"msg": "All good"}


@router.get("/user/{user_id}")
async def get_user_info(user_id: int, session: AsyncGameSession) -> User:
    """Получение информации о пользователе"""

    async with session.begin():
        user = await get_user(user_id, session)
        return user


@router.get("/group/{group_id}")
async def get_group_info(group_id: int, session: AsyncGameSession) -> Group:
    """Получение информации о группе"""

    async with session.begin():
        group = await get_group(group_id, session)
        return group
