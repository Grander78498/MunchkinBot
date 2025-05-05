"""Модуль для обращения к API."""

import json
from typing import Any
from enum import Enum
import requests
import aiohttp
import asyncio
import time


class Method(str, Enum):
    """Перечисление для доступных HTTP методов."""

    GET = "get"
    POST = "post"

    def upper(self) -> str:
        """Метод, чтобы requests мог вызвать его у себя под капотом."""
        return str.upper(self.value)


class APIClient(object):
    """Класс обработки обращений к API."""

    def __new__(cls, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(APIClient, cls).__new__(cls, **kwargs)
        return cls.instance

    def __init__(self, base_url: str | None = None):
        """Класс обработки обращений к API."""
        if base_url is not None:
            self.base_url = base_url
            self.session = aiohttp.ClientSession(base_url=base_url)

    async def __aenter__(self):
        return self
    
    async def __aexit__(self, *args):
        await self.session.close()

    async def _handle_request(
        self,
        method: Method,
        url: str,
        path_params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Отправка запроса с заданными параметрами.

        Args:
            method (Method): Используемый HTTP метод
            url (str): Эндпоинт для отправки запроса

            path_params (dict[str, Any] | None, optional):
            Путевые параметры запроса (которые передаются после ?). Могут отсутствовать

            body (dict[str, Any] | None, optional): Тело запроса. Может отсутствовать

        Returns:
            dict[str, Any]: Ответ от сервера.
        """
        try:
            if path_params is not None:
                params = '&'.join([f'{key}={value}' for key, value in path_params.items() if value is not None])
            else:
                params = ""
            
            async with self.session.request(
                method=method,
                url=url,
                params=params,
                json=body,
                timeout=1
            ) as response:
                # if path_params is None:
                #     response = requests.request(
                #         method=method,
                #         url=self.base_url + url,
                #         data=json.dumps(body),
                #         timeout=1,
                #     )
                # else:
                #     response = requests.request(
                #         method=method,
                #         url=self.base_url + url,
                #         params='&'.join([f'{key}={value}' for key, value in path_params.items() if value is not None]),
                #         data=json.dumps(body),
                #         timeout=1,
                #     )
                status_code = response.status
                result = await response.json()
                if status_code != 200:
                    return {"ok": False, **result}
                return {"ok": True, 'result': result}
        except requests.exceptions.ConnectTimeout:
            return {"ok": False, "detail": "API error"}

    async def save_user(
        self, tg_id: int, user_name: str | None, full_name: str
    ) -> Any:
        """Сохранение юзера."""
        result = await self._handle_request(
            Method.POST,
            "/telegram/user",
            body={
                "tg_id": tg_id,
                "user_name": user_name,
                "full_name": full_name,
            },
        )
        return result

    async def get_user(self, tg_id: int) -> Any:
        """Получение информации о пользователе."""
        result = await self._handle_request(Method.GET, f"/telegram/user/{tg_id}")
        return result
    
    async def create_game(self, creator_id: int) -> Any:
        """Создание игровой партии."""
        result = await self._handle_request(Method.POST, f"/game", path_params={'creator_id': creator_id})
        return result
    
    async def add_user_to_game(self, game_code: str, user_id: int) -> Any:
        """Добавление пользователя в партию."""
        result = await self._handle_request(Method.POST, f"/game/{game_code}/munchkin", path_params={'user_id': user_id})
        return result
    
    async def get_user_games(self, user_id: int, active: bool | None = None) -> Any:
        """Получение манчкинов пользователя"""
        result = await self._handle_request(Method.GET, f"/game/munchkin", path_params={'user_id': user_id, 'active': active})
        return result
    
    async def get_active_user_game(self, user_id: int) -> Any:
        result = await self._handle_request(Method.GET, f"/game", path_params={'user_id': user_id})
        return result
