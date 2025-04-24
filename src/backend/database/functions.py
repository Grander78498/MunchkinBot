"""
Часто используемые функции обращения к БД
"""

from fastapi import HTTPException
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.users import User, Group
from backend.database.game import Game


async def get_user(user_id: int, session: AsyncSession) -> User:
    """ Получение пользователя по tg_id
    
    args:
        user_id: int - tg_id пользователя
    returns:
        User - информация о пользователе из БД
    raises:
        HTTPException - если пользователя нет в БД
    """
    result = await session.execute(select(User).where(User.tg_id == user_id))
    user = result.scalar()
    if user is None:
        raise HTTPException(status_code=404,
                            detail="Пользователя с таким tg_id не существует")

    return user


async def get_group(group_id: int, session: AsyncSession) -> Group:
    """ Получение группы по tg_id
    
    args:
        group_id: int - tg_id группы
    returns:
        Group - информация о группы из БД
    raises:
        HTTPException - если группы нет в БД
    """
    result = await session.execute(
        select(Group).where(Group.tg_id == group_id))
    group = result.scalar()
    if group is None:
        raise HTTPException(status_code=404,
                            detail="Группы с таким tg_id не существует")

    return group


async def get_game(game_id: int, session: AsyncSession) -> Game:
    """ Получение информации об игровой партии по game_id
    
    args:
        game_id: int
    returns:
        Game - информация об игре из БД
    raises:
        HTTPException - если игровой партии нет в БД
    """
    result = await session.execute(select(Game).where(Game.id == game_id))
    game = result.scalar()
    if game is None:
        raise HTTPException(status_code=404,
                            detail="Игры с таким id не существует")
    return game
