from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, Double, Text, LargeBinary, func
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

class Finding(Base):
    __tablename__ = "findings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # 🆕 User-Relation
    species = Column(Text, nullable=True)
    note = Column(Text, nullable=True)
    lat = Column(Double, nullable=True)
    lng = Column(Double, nullable=True)
    taken_at = Column(DateTime(timezone=True), nullable=True)
    image_bytes = Column(LargeBinary, nullable=False)
    image_mime = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Optional: Rückbeziehung, falls du User-Modell hast
    user = relationship("User", back_populates="findings", lazy="joined")



