"""Модуль для обращения к API."""

import json
from typing import Any
from enum import Enum
import requests


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

    def _handle_request(
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
            if path_params is None:
                response = requests.request(
                    method=method,
                    url=self.base_url + url,
                    data=json.dumps(body),
                    timeout=1,
                )
            else:
                response = requests.request(
                    method=method,
                    url=self.base_url + url,
                    params='&'.join([f'{key}={value}' for key, value in path_params.items()]),
                    data=json.dumps(body),
                    timeout=1,
                )
            
            if response.status_code != 200:
                return {"ok": False, **response.json()}
            return {"ok": True, **response.json()}
        except requests.exceptions.ConnectTimeout:
            return {"ok": False, "msg": "API error"}

    def save_user(
        self, tg_id: int, user_name: str | None, full_name: str
    ) -> Any:
        """Сохранение юзера."""
        result = self._handle_request(
            Method.POST,
            "/telegram/user",
            body={
                "tg_id": tg_id,
                "user_name": user_name,
                "full_name": full_name,
            },
        )
        return result

    def get_user(self, tg_id: int) -> Any:
        """Получение информации о пользователе."""
        result = self._handle_request(Method.GET, f"/telegram/user/{tg_id}")
        return result
    
    def create_game(self, creator_id: int) -> Any:
        """Создание игровой партии."""
        result = self._handle_request(Method.POST, f"/game", path_params={'creator_id': creator_id})
        return result
    
    def add_user_to_game(self, game_code: str, user_id: int):
        """Добавление пользователя в партию."""
        result = self._handle_request(Method.POST, f"/game/{game_code}/munchkin", path_params={'user_id': user_id})
        return result
