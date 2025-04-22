"""
Получение информации о манчкине
"""
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, HTTPException
from sqlmodel import select

from backend.database import AsyncGameSession
from backend.database.users import User, UserBase, Group, GroupBase
from backend.database.game import Munchkin, Game
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
        db_group = result.scalar()
        if db_group is None:
            raise HTTPException(status_code=404,
                                detail="Группы с таким tg_id не существует")
        game = Game(group=db_group)
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
            db_user = result.scalar()
            if db_user is None:
                raise HTTPException(
                    status_code=404,
                    detail="Пользователя с таким tg_id не существует")

            result = await session.execute(
                select(Game).where(Game.id == game_id))
            game = result.scalar()
            if game is None:
                raise HTTPException(status_code=404,
                                    detail="Игры с таким id не существует")

            munchkin = Munchkin(user=db_user, game=game)
            session.add(munchkin)
    except IntegrityError as e:
        raise HTTPException(
            status_code=404,
            detail="Пользователь уже есть в данной игровой партии") from e

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
