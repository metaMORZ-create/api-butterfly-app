from pydantic import BaseModel
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