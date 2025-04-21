"""
Главный файл для FastAPI сервера
Управляет жизненным циклом приложения и роутерами
"""
from typing import Any

from fastapi import FastAPI
from backend.routers import users

app = FastAPI()
app.include_router(users.router)


@app.get('/')
async def main() -> Any:
    """Не смотрите сюда"""
    return {'msg': 'Сосал?'}
