# routers/uploads.py
import os
import io
from datetime import datetime
from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc

import cloudinary
import cloudinary.uploader

from db import get_db
import models as tables

router = APIRouter()

# gleiche Dependency-Schreibweise wie in users
db_dependency = Annotated[Session, Depends(get_db)]

# Cloudinary-Config aus Env (Railway Variables / .env)
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)

FOLDER = os.getenv("CLOUDINARY_FOLDER", "uploads")
MAX_BYTES = 8 * 1024 * 1024  # 8 MB

@router.post("")
async def upload_photo(
    db: db_dependency,
    file: UploadFile = File(...),
    user_id: int = Form(...),
    butterfly_id: int = Form(...),
    taken_at: datetime = Form(...),     # ISO-8601: 2025-04-29T10:15:00Z
    latitude: float = Form(...),
    longitude: float = Form(...),
):
    # einfache Validierung wie bei dir im Stil: klare Fehler
    if file.content_type not in {"image/jpeg", "image/png", "image/webp", "image/heic", "image/heif"}:
        raise HTTPException(status_code=415, detail=f"Unsupported media type: {file.content_type}")

    # Dateigröße limitieren
    chunk = await file.read(MAX_BYTES + 1)
    if len(chunk) > MAX_BYTES:
        raise HTTPException(status_code=413, detail="File too large (max 8MB)")
    buffer = io.BytesIO(chunk)

    try:
        # 1) Upload zu Cloudinary
        up = cloudinary.uploader.upload(
            buffer,
            folder=FOLDER,
            resource_type="image",
            overwrite=True,
        )
        image_url = up["secure_url"]
        public_id = up["public_id"]

        # 2) In Postgres speichern (ähnlich wie bei create_user)
        row = tables.ButterflyPhoto(
            user_id=user_id,
            butterfly_id=butterfly_id,
            taken_at=taken_at,
            latitude=latitude,
            longitude=longitude,
            image_url=image_url,
            public_id=public_id,
        )
        db.add(row)
        db.commit()
        db.refresh(row)

        # 3) Antwort im selben Stil: message + Felder
        return {
            "message": "Photo uploaded & saved",
            "id": row.id,
            "user_id": row.user_id,
            "butterfly_id": row.butterfly_id,
            "taken_at": row.taken_at,
            "latitude": row.latitude,
            "longitude": row.longitude,
            "image_url": row.image_url,
            "public_id": row.public_id,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload/Save failed: {e}")
    
@router.get("/user/{user_id}")
def list_user_uploads(
    user_id: int,
    db: db_dependency,
    limit: int = 50,          # Pagination
    offset: int = 0,
    sort: str = "desc",       # "asc" | "desc" nach taken_at
    with_butterfly: bool = True,
):
    # (Optional) prüfen, ob der User existiert
    user = db.query(tables.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    order_by = desc(tables.ButterflyPhoto.taken_at) if sort.lower() == "desc" else asc(tables.ButterflyPhoto.taken_at)

    rows: List[tables.ButterflyPhoto] = (
        db.query(tables.ButterflyPhoto)
        .filter(tables.ButterflyPhoto.user_id == user_id)
        .order_by(order_by)
        .offset(offset)
        .limit(limit)
        .all()
    )

    # Antwort-Shape im gleichen Stil wie dein Upload-Endpoint
    data = []
    for r in rows:
        item = {
            "id": r.id,
            "user_id": r.user_id,
            "butterfly_id": r.butterfly_id,
            "taken_at": r.taken_at,
            "latitude": r.latitude,
            "longitude": r.longitude,
            "image_url": r.image_url,
            "public_id": r.public_id,
        }
        if with_butterfly and r.butterfly:
            item["butterfly"] = {
                "id": r.butterfly.id,
                "common_name": r.butterfly.common_name,
                "scientific_name": r.butterfly.scientific_name,
                "image_url": r.butterfly.image_url,
                "thumbnail_url": r.butterfly.thumbnail_url,
            }
        data.append(item)

    return {
        "message": "OK",
        "user_id": user_id,
        "count": len(data),
        "limit": limit,
        "offset": offset,
        "sort": sort,
        "items": data,
    }
