"""Получение информации о манчкине."""

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from pydantic import BaseModel

from backend.database import AsyncGameSession
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


class MunchkinList(BaseModel):
    munchkins: list[Munchkin]


class UserList(BaseModel):
    users: list[User]


@router.post("")
async def create_game(creator_id: int, session: AsyncGameSession) -> Game:
    """Создание игровой партии пользователем."""
    async with session.begin():
        user = await get_user(session, user_id=creator_id)
        code = await generate_game_code(session)
        game = Game(creator=user, code=code)
        session.add(game)

        munchkin = Munchkin(game=game, user=user)
        session.add(munchkin)

    return game


@router.get("")
async def get_active_game(user_id: int, session: AsyncGameSession) -> Game | None:
    """Создание игровой партии пользователем."""
    async with session.begin():
        game = await get_active_user_game(user_id, session)
        return game


@router.get("/munchkin", response_model=MunchkinList)
async def get_user_munchkins(
    user_id: int, session: AsyncGameSession, active: bool | None = None
) -> dict:
    """Получение манчкинов, созданных пользователем."""
    async with session.begin():
        stmt = select(User).where(User.tg_id == user_id).join(Munchkin).join(Game)
        if active is not None:
            stmt = stmt.where(Game.on_going == active)
        result = await session.execute(stmt)
        user = result.scalar()
        if user is None and active is None:
            raise HTTPException(
                status_code=404,
                detail="Такого пользователя не существует",
            )

        if user is None:
            return []
        return {"munhckins": user.munchkins}


@router.post("/{game_code}/munchkin")
async def create_munchkin(game_code: str, user_id: int, session: AsyncGameSession) -> Munchkin:
    """Создание манчкина."""
    try:
        async with session.begin():
            user = await get_user(session, user_id=user_id)
            game = await get_game(game_code, session)

            if user in game.banned_users:
                raise HTTPException(
                    status_code=404,
                    detail="Пользователь забанен",
                )

            if len(game.munchkins) >= 6:
                raise HTTPException(
                    status_code=404,
                    detail="В игре уже набрано слишком много манчкинов, поищите другую игру",
                )

            munchkin = Munchkin(user=user, game=game)
            session.add(munchkin)
    except IntegrityError as e:
        raise HTTPException(
            status_code=404,
            detail="Пользователь уже есть в данной игровой партии",
        ) from e

    return munchkin


@router.get("/{game_code}/munchkin", response_model=UserList)
async def get_game_munchkins(game_code: str, session: AsyncGameSession) -> dict:
    """Получение манкчинов в игре."""
    async with session.begin():
        game = await get_game(game_code, session)
        return {"users": [munchkin.user for munchkin in game.munchkins]}


@router.delete("/{game_code}", response_model=MunchkinList)
async def delete_game(game_code: str, session: AsyncGameSession) -> dict:
    """Удаление игры."""
    async with session.begin():
        game = await get_game(game_code, session)
        munchkins = [munchkin for munchkin in game.munchkins if munchkin.user_id != game.creator_id]
        await session.delete(game)
        return {"munhckins": munchkins}


@router.delete("/{game_code}/munchkin", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_from_game(game_code: str, user_id: int, session: AsyncGameSession) -> None:
    """Удаление пользователя из игры."""
    async with session.begin():
        result = await session.execute(
            select(Munchkin).join(Game).where(Munchkin.user_id == user_id, Game.code == game_code)
        )
        munchkin = result.scalar()
        await session.delete(munchkin)
        return None


@router.post("/{game_code}/munchkin/ban", status_code=status.HTTP_204_NO_CONTENT)
async def ban_munchkin(game_code: str, user_id: int, session: AsyncGameSession) -> None:
    """Бан манчкина."""
    async with session.begin():
        game = await get_game(game_code, session)
        user = await get_user(session, user_id=user_id)
        game.banned_users.append(user)
        session.add(game)
        session.add(user)

        result = await session.execute(
            select(Munchkin).join(Game).where(Munchkin.user_id == user_id, Game.code == game_code)
        )
        munchkin = result.scalar()
        await session.delete(munchkin)
        return None
