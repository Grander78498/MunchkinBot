"""
Получение информации о манчкине
"""

from typing import Any

import sqlalchemy
from fastapi import APIRouter, HTTPException
from sqlmodel import select
from sqlalchemy.orm import selectinload
import asyncpg
from backend.database import AsyncGameSession
from backend.database.models import User, UserBase, Group, GroupBase, Munchkin, Game
from backend.database.responses import SuccessfulResponse

router = APIRouter(
    prefix='/game',
    tags=['Game'],
)


@router.post('')
async def create_game(group: GroupBase, session: AsyncGameSession) -> Game:
    async with session.begin():
        result = await session.execute(
            select(Group).where(Group.tg_id == group.tg_id))
        group = result.scalar()
        game = Game(group=group)
        if game is None:
            raise HTTPException(status_code=404,
                                detail="Группы с таким tg_id не существует")
        session.add(game)

    return game


@router.get('/munchkin')
async def get_user_munchkins(user_id: int,
                             session: AsyncGameSession) -> list[Munchkin]:
    async with session.begin():
        result = await session.execute(
            select(User).where(User.tg_id == user_id))
        user = result.scalar()
        if user is None:
            raise HTTPException(
                status_code=404,
                detail="Пользователя с таким tg_id не существует")
        return user.munchkins


@router.post('/{game_id}/munchkin')
async def create_munchkin(game_id: int, user: UserBase,
                          session: AsyncGameSession) -> Munchkin:
    try:
        async with session.begin():
            result = await session.execute(
                select(User).where(User.tg_id == user.tg_id))
            user = result.scalar()
            if user is None:
                raise HTTPException(
                    status_code=404,
                    detail="Пользователя с таким tg_id не существует")

            result = await session.execute(
                select(Game).where(Game.id == game_id))
            game = result.scalar()
            if game is None:
                raise HTTPException(status_code=404,
                                    detail="Игры с таким id не существует")

            munchkin = Munchkin(user=user, game=game)
            session.add(munchkin)
    except sqlalchemy.exc.IntegrityError as e:
        raise HTTPException(
            status_code=404,
            detail="Пользователь уже есть в данной игровой партии")

    return munchkin


@router.get('/{game_id}/munchkin')
async def get_game_munchkins(game_id: int,
                             session: AsyncGameSession) -> list[Munchkin]:
    async with session.begin():
        result = await session.execute(select(Game).where(Game.id == game_id))
        game = result.scalar()
        if game is None:
            raise HTTPException(status_code=404,
                                detail="Игры с таким id не существует")
        return game.munchkins
