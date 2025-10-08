from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Float, DateTime, Enum, JSON
from db import Base
from datetime import datetime
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    disabled = Column(Boolean, default=False)
    hashed_password = Column(String)



