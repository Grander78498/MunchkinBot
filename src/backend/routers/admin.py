"""
Управление карточками
"""

from typing import Any

from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, HTTPException
from sqlmodel import select
import asyncpg
from backend.database import AsyncGameSession
from backend.database.models import ItemBase, ItemCreate, Item, Card
from backend.database.responses import SuccessfulResponse

router = APIRouter(
    prefix='/admin',
    tags=['Admin game'],
)

@router.post('/item')
async def create_item(item: ItemCreate, session: AsyncGameSession) -> Item:
    try:
        async with session.begin():
            db_card = Card.model_validate(item)
            session.add(db_card)

            db_item = Item(card=db_card, **item.model_dump())
            session.add(db_item)
        
        return db_item
    except IntegrityError:
        raise HTTPException(
            status_code=404,
            detail="Присутствуют повторяющиеся поля в карточке")