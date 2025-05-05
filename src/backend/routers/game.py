"""Получение информации о манчкине."""
from typing import Any

from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from fastapi import APIRouter, HTTPException

from backend.database import AsyncGameSession
from backend.database.responses import SuccessfulResponse
from backend.database.game import Munchkin, Game
from backend.database.users import User
from backend.utils.db_functions import (
    get_user,
    get_game,
    generate_game_code,
    get_active_user_game,
)

router = APIRouter(
    prefix="/game",
    tags=["Game"],
)


@router.post("")
async def create_game(creator_id: int, session: AsyncGameSession) -> Game:
    """Создание игровой партии пользователем."""
    async with session.begin():
        user = await get_user(creator_id, session)
        code = await generate_game_code(session)
        game = Game(creator=user, code=code)
        session.add(game)

        munchkin = Munchkin(game=game, user=user)
        session.add(munchkin)

    return game


@router.get("")
async def get_active_game(
    user_id: int, session: AsyncGameSession
) -> Game | None:
    """Создание игровой партии пользователем."""
    async with session.begin():
        game = await get_active_user_game(user_id, session)
        return game


@router.get("/munchkin")
async def get_user_munchkins(
    user_id: int, session: AsyncGameSession, active: bool | None = None
) -> list[Munchkin]:
    """Получение манчкинов, созданных пользователем."""
    async with session.begin():
        stmt = (
            select(User)
            .where(User.tg_id == user_id)
            .join(Munchkin, Munchkin.user_id == User.tg_id)
            .join(Game, Game.id == Munchkin.game_id)
        )
        if active is not None:
            stmt = stmt.where(Game.on_going == active)
        result = await session.execute(stmt)
        user = result.scalar()
        if user is None and active is None:
            raise HTTPException(
                status_code=404,
                detail="Такого пользователя не существует",
            )
        elif user is None:
            return []
        return user.munchkins


@router.post("/{game_code}/munchkin")
async def create_munchkin(
    game_code: str, user_id: int, session: AsyncGameSession
) -> Munchkin:
    """Создание манчкина."""
    try:
        async with session.begin():
            user = await get_user(user_id, session)
            game = await get_game(game_code, session)

            munchkin = Munchkin(user=user, game=game)
            session.add(munchkin)
    except IntegrityError as e:
        raise HTTPException(
            status_code=404,
            detail="Пользователь уже есть в данной игровой партии",
        ) from e

    return munchkin


@router.get("/{game_id}/munchkin")
async def get_game_munchkins(
    game_id: int, session: AsyncGameSession
) -> list[Munchkin]:
    """Получение манкчинов в игре."""
    async with session.begin():
        game = await get_game(game_id, session)
        return game.munchkins


@router.delete("/{game_code}", response_model=SuccessfulResponse)
async def delete_game(game_code: str, session: AsyncGameSession) -> Any:
    async with session.begin():
        game = await get_game(game_code, session)
        await session.delete(game)
        return {'msg': 'Удалено'}
    

@router.delete("/{game_code}/munchkin", response_model=SuccessfulResponse)
async def delete_user_from_game(game_code: str, user_id: int, session: AsyncGameSession) -> Any:
    async with session.begin():
        result = await session.execute(select(Munchkin).join(Game, Game.id == Munchkin.game_id).where(Munchkin.user_id == user_id, Game.code == game_code))
        munchkin = result.scalar()
        await session.delete(munchkin)
        return {'msg': 'Удалено'}