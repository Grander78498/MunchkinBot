"""Получение информации о манчкине."""

from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, HTTPException

from backend.database import AsyncGameSession
from backend.database.functions import get_user, get_group, get_game
from backend.database.game import Munchkin, Game

router = APIRouter(
    prefix="/game",
    tags=["Game"],
)


@router.post("")
async def create_game(group_id: int, session: AsyncGameSession) -> Game:
    """Создание игровой партии в группе."""
    async with session.begin():
        group = await get_group(group_id, session)
        game = Game(group=group)
        session.add(game)

    return game


@router.get("/munchkin")
async def get_user_munchkins(
    user_id: int, session: AsyncGameSession
) -> list[Munchkin]:
    """Получение манчкинов, созданных пользователем."""
    async with session.begin():
        user = await get_user(user_id, session)
        return user.munchkins


@router.post("/{game_id}/munchkin")
async def create_munchkin(
    game_id: int, user_id: int, session: AsyncGameSession
) -> Munchkin:
    """Создание манчкина."""
    try:
        async with session.begin():
            user = await get_user(user_id, session)
            game = await get_game(game_id, session)

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
