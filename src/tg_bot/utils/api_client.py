"""
Модуль для обращения к API
"""

import json
from typing import Any
from enum import Enum
import requests


class Method(Enum):
    """Перечисление для доступных HTTP методов"""

    GET = 'get'
    POST = 'post'

    def upper(self):
        """Метод, чтобы requests мог вызвать его у себя под капотом"""
        return str.upper(self.value)


class APIClient:
    """Класс обработки обращений к API"""

    def __init__(self, base_url: str):
        self.base_url = base_url

    def _handle_request(self,
                        method: Method,
                        url: str,
                        path_params: dict[str, Any] | None = None,
                        body: dict[str, Any] | None = None) -> dict[str, Any]:
        """Отправка запроса с заданными параметрами

        Args:
            method (Method): Используемый HTTP метод
            url (str): Эндпоинт для отправки запроса

            path_params (dict[str, Any] | None, optional): 
            Путевые параметры запроса (которые передаются после ?). Могут отсутствовать

            body (dict[str, Any] | None, optional): Тело запроса. Может отсутствовать

        Returns:
            dict[str, Any]: Ответ от сервера
        """

        response = requests.request(method=method,
                                    url=self.base_url + url,
                                    params=json.dumps(path_params),
                                    data=json.dumps(body),
                                    timeout=1)
        return response.json()

    def save_user(self, tg_id: int, user_name: str,
                  full_name: str) -> dict[str, Any]:
        """Сохранение юзера

        Args:
            tg_id (int): tg_id
            user_name (str): Краткое имя
            full_name (str): Имя и фамилия

        Returns:
            dict[str, Any]: Статус сохранения
        """
        result = self._handle_request(Method.POST,
                                      '/user',
                                      body={
                                          'tg_id': tg_id,
                                          'user_name': user_name,
                                          'full_name': full_name
                                      })
        return result

    def get_user(self, tg_id: int) -> dict[str, Any]:
        """Получение информации о пользователе

        Args:
            tg_id (int): id искомого пользователя

        Returns:
            dict[str, Any]: Информация о пользователе или информация об ошибке
        """
        result = self._handle_request(Method.GET, f'/user/{tg_id}')
        return result
