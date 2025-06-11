"""Модели ответов от API."""

from pydantic import BaseModel


class User(BaseModel):
    """Класс пользователя."""

    tg_id: int
    user_name: str
    full_name: str


class Game(BaseModel):
    """Класс игровой партии."""

    id: int
    code: str
    creator_id: int
    on_going: bool
    current_player_number: int


class Munchkin(BaseModel):
    """Класс манчкина."""

    id: int
    user_id: int
    game_id: int
    gender: str
    number: int
    level: int
    strength: int
    luck: int
    runaway_bonus: int


class UserList(BaseModel):
    """Список пользователей."""

    users: list[User]


class MunchkinList(BaseModel):
    """Список манчкинов."""

    munchkins: list[Munchkin]
