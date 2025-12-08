from typing import Tuple, List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Category
from tgstat_client import tgstat_client


async def fetch_categories_from_api() -> List[dict]:
    """Получает категории из TGStat API."""
    data = await tgstat_client.get("/database/categories")

    if data.get("error"):
        status_code = data.get("status_code") or 502
        raise HTTPException(status_code=status_code, detail=data["error"])

    response = data.get("response")
    if not isinstance(response, list):
        raise HTTPException(status_code=502, detail="Некорректный ответ от TGStat API")

    return response


def upsert_categories(db: Session, categories: List[dict]) -> int:
    """Сохраняет категории в БД, обновляя существующие записи."""
    saved = 0
    for item in categories:
        code = item.get("code")
        name = item.get("name")
        if not code or not name:
            continue

        db.merge(Category(code=code, name=name))
        saved += 1

    db.commit()
    return saved


async def sync_categories(db: Session) -> Tuple[int, List[Category]]:
    """Синхронизирует категории из TGStat и возвращает сохраненный список."""
    categories = await fetch_categories_from_api()
    saved_count = upsert_categories(db, categories)
    db_categories = db.query(Category).order_by(Category.name).all()
    return saved_count, db_categories