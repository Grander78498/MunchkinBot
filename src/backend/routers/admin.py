"""
Управление карточками
"""

from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, HTTPException
from backend.database import AsyncGameSession
from backend.database.cards import ItemCreate, Item, Card

router = APIRouter(
    prefix="/admin",
    tags=["Admin game"],
)


@router.post("/item")
async def create_item(item: ItemCreate, session: AsyncGameSession) -> Item:
    """Создание шмотки"""
    try:
        async with session.begin():
            db_card = Card.model_validate(item)
            session.add(db_card)

            db_item = Item(card=db_card, **item.model_dump())
            session.add(db_item)

        return db_item
    except IntegrityError as e:
        raise HTTPException(
            status_code=404, detail="Присутствуют повторяющиеся поля в карточке"
        ) from e
