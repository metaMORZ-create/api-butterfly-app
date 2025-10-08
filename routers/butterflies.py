from fastapi import APIRouter, Depends, HTTPException, Query, Form
from typing import Annotated, Optional, List
from sqlalchemy.orm import Session
from typevalidation import ButterflyOut
import json

from db import get_db
import models as tables

router = APIRouter()
db_dependency = Annotated[Session, Depends(get_db)]

# ---------- Helpers ----------
def _parse_json_field(raw: Optional[str]) -> Optional[list]:
    if raw is None or raw == "":
        return None
    try:
        val = json.loads(raw)
        if isinstance(val, list):
            return val
        # einfache Komma-Liste als Fallback akzeptieren
        if isinstance(val, str):
            return [s.strip() for s in val.split(",") if s.strip()]
    except json.JSONDecodeError:
        # "tag1, tag2" supporten
        return [s.strip() for s in raw.split(",") if s.strip()]
    return None

# ---------- Endpoints ----------
@router.post("/create", response_model=dict, summary="Schmetterling anlegen (Form-POST)")
def create_butterfly(
    db: db_dependency,
    common_name: str = Form(...),
    scientific_name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    reproduction: Optional[str] = Form(None),
    habitat: Optional[str] = Form(None),
    season: Optional[str] = Form(None),
    wingspan_min_mm: Optional[int] = Form(None),
    wingspan_max_mm: Optional[int] = Form(None),
    image_url: Optional[str] = Form(None),
    thumbnail_url: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),              # JSON-String oder "a,b,c"
    regions: Optional[str] = Form(None),           # JSON-String oder "x,y"
    protection_status: Optional[str] = Form(None),
):
    # Optionaler Unique-Check
    existing = (
        db.query(tables.Butterfly)
        .filter(
            tables.Butterfly.common_name == common_name,
            tables.Butterfly.scientific_name == scientific_name,
        )
        .first()
    )
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
        tags=_parse_json_field(tags),
        regions=_parse_json_field(regions),
        protection_status=protection_status,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return {"message": "Butterfly created", "id": obj.id}

@router.get("/{butterfly_id}", response_model=ButterflyOut, summary="Einzelnen Schmetterling holen")
def get_butterfly(butterfly_id: int, db: db_dependency):
    b = db.get(tables.Butterfly, butterfly_id)
    if not b:
        raise HTTPException(status_code=404, detail="Not found")
    return b

@router.get("/", response_model=List[ButterflyOut], summary="Liste aller Schmetterlinge")
def list_butterflies(q: Optional[str] = Query(None), db: db_dependency = None):
    qry = db.query(tables.Butterfly)
    if q:
        like = f"%{q}%"
        qry = qry.filter(
            (tables.Butterfly.common_name.ilike(like))
            | (tables.Butterfly.scientific_name.ilike(like))
            | (tables.Butterfly.description.ilike(like))
        )
    return qry.order_by(tables.Butterfly.common_name.asc()).all()
