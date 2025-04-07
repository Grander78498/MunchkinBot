import requests
import json
from typing import Any
from enum import Enum


class Method(Enum):
    GET = 'get'
    POST = 'post'

    def upper(self):
        return str.upper(self.value)


class APIClient:

    def __init__(self, base_url: str):
        self.base_url = base_url

    def _handle_request(self,
                        method: Method,
                        url: str,
                        path_params: dict[str, Any] | None = None,
                        body: dict[str, Any] | None = None) -> dict[str, Any]:
        response = requests.request(method=method,
                                    url=self.base_url + url,
                                    params=json.dumps(path_params),
                                    data=json.dumps(body))
        return response.json()

    def save_user(self, tg_id: int, user_name: str) -> dict[str, Any]:
        result = self._handle_request(Method.POST,
                                      '/users/save',
                                      body=dict(tg_id=tg_id,
                                                user_name=user_name))
        return result
