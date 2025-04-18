from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models import User, get_session


router = APIRouter(
    prefix='/users',
    tags=['users'],
)


@router.post('/save')
async def save_user(user: User, session: Annotated[AsyncSession, Depends(get_session)]):
    async with session.begin():
        session.add(user)
    return {'msg': "All good"}