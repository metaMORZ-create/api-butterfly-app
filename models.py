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

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String, index=True)  # z.B. zufällige UUID oder Session-ID
    user = Column(String)  # "user" oder "system"
    user_id = Column(Integer, nullable=True)  # falls eingeloggt, sonst None
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

