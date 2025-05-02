"""Модуль для кастомных ответов сервера."""

from pydantic import BaseModel


class SuccessfulResponse(BaseModel):
    """Успешный ответ в случае, когда ничего возвращать не нужно."""

    msg: str
