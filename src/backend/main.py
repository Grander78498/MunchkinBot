from contextlib import asynccontextmanager
from fastapi import FastAPI
from backend.models import (
    create_game_tables, 
    create_cards_tables
)
from backend.routers import users


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_game_tables()
    await create_cards_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(users.router)


@app.get('/')
async def main():
    return {'msg': 'Сосал?'}