from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, Float
from db import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    disabled = Column(Boolean, default=False)
    hashed_password = Column(String)

class ButterflyPhoto(Base):
    __tablename__ = "butterfly_photos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    butterfly_id = Column(Integer, nullable=False, index=True)
    taken_at = Column(DateTime(timezone=True), nullable=False)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # optional aber praktisch:
    image_url = Column(String, nullable=False)
    public_id = Column(String, nullable=False)



