from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: str
    disabled: bool = False
    password: str

class LoginUser(BaseModel):
    username: str
    password: str

class FindingMeta(BaseModel):
    user_id: int                         # <-- kommt vom Client
    species: Optional[str] = None
    note: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    taken_at: Optional[datetime] = None  # ISO-8601 String vom Client

class FindingOut(BaseModel):
    id: int
    user_id: int
    species: Optional[str] = None
    note: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    taken_at: Optional[datetime] = None
    created_at: datetime
    image_url: str

class ButterflyOut(BaseModel):
    id: int
    common_name: str
    scientific_name: Optional[str] = None
    description: Optional[str] = None
    reproduction: Optional[str] = None
    habitat: Optional[str] = None
    season: Optional[str] = None
    wingspan_min_mm: Optional[int] = Field(None, ge=0)
    wingspan_max_mm: Optional[int] = Field(None, ge=0)
    image_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    tags: Optional[list] = None           # JSONB in DB
    regions: Optional[list] = None        # JSONB in DB
    protection_status: Optional[str] = None

    class Config:
        from_attributes = True