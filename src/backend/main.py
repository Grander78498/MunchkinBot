from contextlib import asynccontextmanager
from fastapi import FastAPI
from backend.models import create_tables
from backend.routers import users


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(users.router)


@app.get('/')
async def main():
    return {'msg': 'Сосал?'}