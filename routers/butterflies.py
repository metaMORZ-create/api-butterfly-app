# routers/butterflies.py
from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
import json

from db import get_db
import models as tables

router = APIRouter()
db_dependency = Annotated[Session, Depends(get_db)]

def _parse_list(raw: Optional[str]) -> Optional[list]:
    """Akzeptiert JSON-Array oder 'a, b, c' und gibt eine Liste zurück."""
    if not raw:
        return None
    # Erst versuchen, als JSON zu interpretieren
    try:
        val = json.loads(raw)
        if isinstance(val, list):
            return val
    except json.JSONDecodeError:
        pass
    # Fallback: Komma-getrennte Liste
    return [s.strip() for s in raw.split(",") if s.strip()]

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
    # neu:
    tags: Optional[str] = None,              # JSON-Array oder "a,b,c"
    regions: Optional[str] = None,           # JSON-Array oder "x,y"
    protection_status: Optional[str] = None,
    db: db_dependency = None,
):
    # Unique-Check (common_name + scientific_name)
    existing = db.query(tables.Butterfly).filter(
        tables.Butterfly.common_name == common_name,
        tables.Butterfly.scientific_name == scientific_name
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Butterfly already exists")

    obj = tables.Butterfly(
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
        # Nur setzen, wenn Spalten im Model existieren:
        tags=_parse_list(tags) if hasattr(tables.Butterfly, "tags") else None,
        regions=_parse_list(regions) if hasattr(tables.Butterfly, "regions") else None,
        protection_status=protection_status if hasattr(tables.Butterfly, "protection_status") else None,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return {"message": "Butterfly created", "id": obj.id}

@router.get("/{butterfly_id}")
def get_butterfly(butterfly_id: int, db: db_dependency):
    b = db.query(tables.Butterfly).get(butterfly_id)
    if not b:
        raise HTTPException(status_code=404, detail="Not found")
    return b

@router.get("/catalog")
def get_catalog(
    db: db_dependency,
    limit: int = 1000,     # Standard: viele Einträge, kann auf "alle" erhöht werden
    offset: int = 0,
):
    """
    Gibt den kompletten Artenkatalog zurück (optional paginiert).
    Response: { total, offset, limit, items: [Butterfly, ...] }
    """
    total = db.query(func.count(tables.Butterfly.id)).scalar()
    items = (
        db.query(tables.Butterfly)
        .order_by(tables.Butterfly.common_name.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "items": items,  # FastAPI serialisiert ORM-Objekte automatisch
    }

