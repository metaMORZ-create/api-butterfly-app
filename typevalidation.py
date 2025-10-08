from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: str
    disabled: bool = False
    password: str

class LoginUser(BaseModel):
    username: str
    password: str