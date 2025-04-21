"""
Получение информации о пользователях
"""

from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import select
from backend.database import AsyncGameSession
from backend.database.models import User
from backend.database.responses import SuccessfulResponse

router = APIRouter(
    prefix='/user',
    tags=['user'],
)


@router.post('', response_model=SuccessfulResponse)
async def save_user(user: User, session: AsyncGameSession) -> Any:
    """Сохранение информации о пользователе"""

    async with session.begin():
        session.add(user)

    return {'msg': "All good"}


@router.get('/{user_id}')
async def get_user(user_id: int, session: AsyncGameSession) -> User:
    """Получение информации о пользователе"""

    async with session.begin():
        stmt = select(User).where(User.tg_id == user_id)
        result = await session.execute(stmt)
        user = result.scalar()
        if user is None:
            raise HTTPException(
                status_code=404,
                detail="Пользователя с таким tg_id не существует")
        return user
