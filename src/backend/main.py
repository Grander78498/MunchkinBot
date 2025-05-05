"""
Главный файл для FastAPI сервера.

Управляет жизненным циклом приложения и роутерами.
"""

from typing import Any

from fastapi import FastAPI
from backend.routers import game, telegram, admin, actions, conditions

app = FastAPI()
app.include_router(telegram.router)
app.include_router(game.router)
app.include_router(admin.router)
app.include_router(actions.router)
app.include_router(conditions.router)


@app.get("/")
async def main() -> Any:
    """Не смотрите сюда."""
    return {"msg": "Сосал?"}
