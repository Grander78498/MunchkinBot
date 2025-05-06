"""Часто используемые функции обращения к БД."""

import secrets
import string

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from backend.database.actions import Action
from backend.database.conditions import Condition
from backend.database.game import Game, Munchkin
from backend.database.users import User
from custom_exceptions.general import CodeGenerationException


async def get_user(session: AsyncSession, user_id: int | None = None, user_name: str | None = None) -> User:
    """Получение пользователя по tg_id.

    args:
        user_id: int - tg_id пользователя
        user_name: str - краткое имя пользователя
    returns:
        User - информация о пользователе из БД
    raises:
        HTTPException - если пользователя нет в БД
    """
    if user_id is not None:
        result = await session.execute(select(User).where(User.tg_id == user_id))
    elif user_name is not None:
        result = await session.execute(select(User).where(User.user_name == user_name))
    else:
        raise HTTPException(
            status_code=404, detail="Параметры сосали"
        )

    user = result.scalar()
    if user is None:
        raise HTTPException(
            status_code=404, detail="Пользователя с таким tg_id или user_name не существует"
        )

    return user


async def get_game(game_code: str, session: AsyncSession) -> Game:
    """Получение информации об игровой партии по коду приглашения.

    args:
        game_code: str - код приглашения
    returns:
        Game - информация об игре из БД
    raises:
        HTTPException - если игровой партии нет в БД
    """
    result = await session.execute(select(Game).where(Game.code == game_code))
    game = result.scalar()
    if game is None:
        raise HTTPException(
            status_code=404,
            detail="Игры с таким кодом приглашения не существует",
        )
    return game


async def get_active_user_game(
        user_id: int, session: AsyncSession
) -> Game | None:
    result = await session.execute(
        select(Game)
        .where(Game.on_going == True)
        .join(Munchkin, Munchkin.game_id == Game.id)
        .join(User, User.tg_id == Munchkin.user_id)
        .where(User.tg_id == user_id)
    )
    game = result.scalar()
    return game


async def get_action(action_id: int, session: AsyncSession) -> Action:
    """Получение информации о действии по его id.

    args:
        action_id: int
    returns:
        Action - информация о действии из БД
    raises:
        HTTPException - если действия нет в БД
    """
    result = await session.execute(select(Action).where(Action.id == action_id))
    action = result.scalar()
    if action is None:
        raise HTTPException(
            status_code=404, detail="Действия с таким id не существует"
        )
    return action


async def get_condition(condition_id: int, session: AsyncSession) -> Condition:
    """Получение информации об условии по его id.

    args:
        condition_id: int
    returns:
        Condition - информация об условии из БД
    raises:
        HTTPException - если условия нет в БД
    """
    result = await session.execute(
        select(Condition).where(Condition.id == condition_id)
    )
    condition = result.scalar()
    if condition is None:
        raise HTTPException(
            status_code=404, detail="Условия с таким id не существует"
        )
    return condition


async def generate_game_code(
        session: AsyncSession, length: int = 6, attempts: int = 100
) -> str:
    """Генерация случайного кода игры."""
    alphabet = string.ascii_uppercase + string.digits

    while True:
        code = "".join(secrets.choice(alphabet) for _ in range(length))
        for _ in range(attempts):
            game = (
                await session.execute(select(Game).where(Game.code == code))
            ).scalar()
            if game is None:
                return code
            code = "".join(secrets.choice(alphabet) for _ in range(length))
        length += 1
        if length > 20:
            raise CodeGenerationException(
                "Превышена допустимая длина генерируемого кода игры"
            )
