from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, Optional, List
from sqlalchemy.orm import Session
from db import get_db
import models as tables

router = APIRouter()
db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/create")
def create_butterfly(
    common_name: str,
    scientific_name: Optional[str] = None,
    description: Optional[str] = None,
    reproduction: Optional[str] = None,
    habitat: Optional[str] = None,
    season: Optional[str] = None,
    wingspan_min_mm: Optional[int] = None,
    wingspan_max_mm: Optional[int] = None,
    image_url: Optional[str] = None,
    thumbnail_url: Optional[str] = None,
    db: db_dependency = None,
):
    # optional: Unique-Check auf common_name + scientific_name
    existing = db.query(tables.Butterfly).filter(
        tables.Butterfly.common_name == common_name,
        tables.Butterfly.scientific_name == scientific_name
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Butterfly already exists")

    b = tables.Butterfly(
        common_name=common_name,
        scientific_name=scientific_name,
        description=description,
        reproduction=reproduction,
        habitat=habitat,
        season=season,
        wingspan_min_mm=wingspan_min_mm,
        wingspan_max_mm=wingspan_max_mm,
        image_url=image_url,
        thumbnail_url=thumbnail_url,
    )
    db.add(b)
    db.commit()
    db.refresh(b)
    return {"message": "Butterfly created", "id": b.id}

@router.get("/{butterfly_id}")
def get_butterfly(butterfly_id: int, db: db_dependency):
    b = db.query(tables.Butterfly).get(butterfly_id)
    if not b:
        raise HTTPException(status_code=404, detail="Not found")
    return b

@router.get("")
def list_butterflies(q: Optional[str] = None, db: db_dependency = None) -> List[tables.Butterfly]:
    qry = db.query(tables.Butterfly)
    if q:
        # einfacher Textfilter
        like = f"%{q}%"
        qry = qry.filter(
            (tables.Butterfly.common_name.ilike(like)) |
            (tables.Butterfly.scientific_name.ilike(like)) |
            (tables.Butterfly.description.ilike(like))
        )
    return qry.order_by(tables.Butterfly.common_name.asc()).all()
