"""Модуль для обращения к API."""

from typing import Any, Literal
import types

import aiohttp
import requests
from pydantic import BaseModel

from tg_bot.settings import get_settings


settings = get_settings()
Method = Literal["GET", "POST", "PUT", "DELETE"]


class APIResponse(BaseModel):
    """Общая модель ответов от API."""

    ok: bool
    detail: str | None = None
    result: dict[str, Any] = {}
    result_list: list[dict[str, Any]] = []


class APIClientException(Exception):
    """Исключение на неправильное использование APIClient."""


class APIClient:
    """Класс обработки обращений к API."""

    def __init__(self, base_url: str | None = None):
        if base_url is None:
            base_url = settings.api_url
        self.base_url = base_url
        self.session: aiohttp.ClientSession | None = None

    async def __aenter__(self) -> "APIClient":
        self.session = aiohttp.ClientSession(
            base_url=self.base_url, timeout=aiohttp.ClientTimeout(total=5)
        )
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> None:
        if self.session is not None:
            await self.session.close()
            self.session = None

    async def _handle_request(
        self,
        method: Method,
        url: str,
        path_params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
    ) -> APIResponse:
        """Отправка запроса с заданными параметрами.

        Параметры:
            method (Method): Используемый HTTP метод
            url (str): Эндпоинт для отправки запроса

            path_params (dict[str, Any] | None, optional):
            Путевые параметры запроса (которые передаются после ?). Могут отсутствовать

            body (dict[str, Any] | None, optional): Тело запроса. Может отсутствовать

        Возвращает:
            dict[str, Any]: Ответ от сервера.
        """
        try:
            if self.session is None:
                raise APIClientException("API Client необходимо вызывать через менеджер контекста")
            if path_params is not None:
                params = "&".join(
                    [f"{key}={value}" for key, value in path_params.items() if value is not None]
                )
            else:
                params = ""

            async with self.session.request(
                method=method, url=url, params=params, json=body
            ) as response:
                status_code = response.status
                result, result_list = {}, []
                match await response.json():
                    case list(tmp):
                        result_list = tmp
                    case dict(tmp):
                        result = tmp
                        if status_code != 200:
                            return APIResponse(ok=False, **result)

                return APIResponse(ok=True, result=result, result_list=result_list)
        except requests.exceptions.ConnectTimeout:
            return APIResponse(ok=False, detail="API Error")

    async def save_user(self, tg_id: int, user_name: str | None, full_name: str) -> APIResponse:
        """Сохранение юзера."""
        result = await self._handle_request(
            "POST",
            "/telegram/user",
            body={
                "tg_id": tg_id,
                "user_name": user_name,
                "full_name": full_name,
            },
        )
        return result

    async def get_user(
        self, user_id: int | None = None, user_name: str | None = None
    ) -> APIResponse:
        """Получение информации о пользователе."""
        params: dict[str, Any] = {}
        if user_id is not None:
            params.update(user_id=user_id)
        if user_name is not None:
            params.update(user_name=user_name)
        result = await self._handle_request("GET", "/telegram/user", path_params=params)
        return result

    async def create_game(self, creator_id: int) -> APIResponse:
        """Создание игровой партии."""
        result = await self._handle_request("POST", "/game", path_params={"creator_id": creator_id})
        return result

    async def add_user_to_game(self, game_code: str, user_id: int) -> APIResponse:
        """Добавление пользователя в партию."""
        result = await self._handle_request(
            "POST",
            f"/game/{game_code}/munchkin",
            path_params={"user_id": user_id},
        )
        return result

    async def get_user_games(self, user_id: int, active: bool | None = None) -> APIResponse:
        """Получение манчкинов пользователя"""
        result = await self._handle_request(
            "GET",
            "/game/munchkin",
            path_params={"user_id": user_id, "active": active},
        )
        return result

    async def get_active_user_game(self, user_id: int) -> APIResponse:
        """Получение активной игры пользователя.

        Параметры:
            user_id (int): id пользователя

        Возвращает:
            APIResponse
        """
        result = await self._handle_request("GET", "/game", path_params={"user_id": user_id})
        return result

    async def delete_game(self, game_code: str) -> APIResponse:
        """Удаление игры.

        Параметры:
            game_code (str): код игры

        Возвращает:
            APIResponse
        """
        result = await self._handle_request("DELETE", f"/game/{game_code}")
        return result

    async def delete_user_from_game(self, game_code: str, user_id: int) -> APIResponse:
        """Удаление пользователя из игры.

        Параметры:
            game_code (str): код игры
            user_id (int): id пользователя

        Возвращает:
            APIResponse
        """
        result = await self._handle_request(
            "DELETE",
            f"/game/{game_code}/munchkin",
            path_params={"user_id": user_id},
        )
        return result

    async def get_munchkins(self, game_code: str) -> APIResponse:
        """Получение списка манчкинов в игре.

        Параметры:
            game_code (str): код игры

        Возвращает:
            APIResponse
        """
        result = await self._handle_request("GET", f"/game/{game_code}/munchkin")
        return result

    async def ban_user(self, game_code: str, user_id: int) -> APIResponse:
        """Бан пользователя из игры.

        Параметры:
            game_code (str): код игры
            user_id (int): id пользователя

        Возвращает:
            APIResponse
        """
        result = await self._handle_request(
            "POST",
            f"/game/{game_code}/munchkin/ban",
            path_params={"user_id": user_id},
        )
        return result
