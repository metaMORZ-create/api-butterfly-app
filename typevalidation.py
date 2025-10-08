from pydantic import BaseModel
from typing import Optional

class QuestionRequest(BaseModel):
    question: str
    chat_id: Optional[str] = None
    user_id: str

class UserBase(BaseModel):
    username: str
    email: str
    disabled: bool = False
    password: str

class LoginUser(BaseModel):
    username: str
    password: str