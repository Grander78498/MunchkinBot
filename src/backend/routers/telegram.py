"""
Получение информации о пользователях
"""

from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import select
from backend.database import AsyncGameSession
from backend.database.models import User, Group
from backend.database.responses import SuccessfulResponse

router = APIRouter(
    prefix='/telegram',
    tags=['Telegram'],
)


@router.post('/user', response_model=SuccessfulResponse)
async def save_user(user: User, session: AsyncGameSession) -> Any:
    """Сохранение информации о пользователе"""

    async with session.begin():
        session.add(user)

    return {'msg': "All good"}


@router.post('/group', response_model=SuccessfulResponse)
async def save_user(group: Group, session: AsyncGameSession) -> Any:
    """Сохранение информации о группе"""

    async with session.begin():
        session.add(group)

    return {'msg': "All good"}


@router.get('/user/{user_id}')
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


@router.get('/group/{group_id}')
async def get_user(group_id: int, session: AsyncGameSession) -> Group:
    """Получение информации о группе"""

    async with session.begin():
        stmt = select(Group).where(Group.tg_id == group_id)
        result = await session.execute(stmt)
        group = result.scalar()
        if group is None:
            raise HTTPException(
                status_code=404,
                detail="Группы с таким tg_id не существует")
        return group