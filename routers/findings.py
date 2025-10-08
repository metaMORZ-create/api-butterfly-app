# routers/findings.py
from __future__ import annotations

import json
from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, Request
from fastapi.responses import Response
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typevalidation import FindingMeta, FindingOut  # <- Pydantic-Schemas

from db import get_db            # <- kommt aus deinem Projekt
from models import Finding       # <- SQLAlchemy-ORM Model (mit user_id-Spalte)

router = APIRouter(prefix="/findings", tags=["findings"])


# --------- Endpoints ----------
@router.post("", response_model=FindingOut, status_code=201)
def create_finding(
    request: Request,
    image: UploadFile = File(..., description="Bilddatei"),
    data: str = Form(..., description="JSON der Finding-Metadaten"),
    db: Session = Depends(get_db),
):
    # Metadaten sicher parsen (Pydantic v1/v2 kompatibel)
    try:
        meta_dict = json.loads(data)
        meta = FindingMeta(**meta_dict)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON in 'data'")

    # Bild lesen
    content = image.file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty image")
    mime = image.content_type or "image/jpeg"

    # Insert via ORM
    row = Finding(
        user_id=meta.user_id,
        species=meta.species,
        note=meta.note,
        lat=meta.lat,
        lng=meta.lng,
        taken_at=meta.taken_at,
        image_bytes=content,
        image_mime=mime,
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    image_url = request.url_for("get_finding_image", finding_id=row.id)
    return FindingOut(
        id=row.id,
        user_id=row.user_id,
        species=row.species,
        note=row.note,
        lat=row.lat,
        lng=row.lng,
        taken_at=row.taken_at,
        created_at=row.created_at,
        image_url=str(image_url),
    )


@router.get("", response_model=List[FindingOut])
def list_findings(
    request: Request,
    db: Session = Depends(get_db),
    user_id: Optional[int] = None,  # optionaler Filter: nur Funde eines Users
    limit: int = 50,
    offset: int = 0,
):
    limit = max(1, min(limit, 200))
    q = db.query(Finding)
    if user_id is not None:
        q = q.filter(Finding.user_id == user_id)
    rows = q.order_by(Finding.created_at.desc()).offset(offset).limit(limit).all()

    out: List[FindingOut] = []
    for r in rows:
        out.append(FindingOut(
            id=r.id,
            user_id=r.user_id,
            species=r.species,
            note=r.note,
            lat=r.lat,
            lng=r.lng,
            taken_at=r.taken_at,
            created_at=r.created_at,
            image_url=str(request.url_for("get_finding_image", finding_id=r.id)),
        ))
    return out


@router.get("/{finding_id}", response_model=FindingOut)
def get_finding(
    request: Request,
    finding_id: int,
    db: Session = Depends(get_db),
):
    r = db.query(Finding).get(finding_id)
    if not r:
        raise HTTPException(status_code=404, detail="Not found")
    return FindingOut(
        id=r.id,
        user_id=r.user_id,
        species=r.species,
        note=r.note,
        lat=r.lat,
        lng=r.lng,
        taken_at=r.taken_at,
        created_at=r.created_at,
        image_url=str(request.url_for("get_finding_image", finding_id=r.id)),
    )


@router.get("/{finding_id}/image", name="get_finding_image")
def get_finding_image(
    finding_id: int,
    db: Session = Depends(get_db),
):
    r = db.query(Finding).get(finding_id)
    if not r:
        raise HTTPException(status_code=404, detail="Not found")
    headers = {"Cache-Control": "public, max-age=86400"}
    return Response(content=r.image_bytes, media_type=r.image_mime, headers=headers)
