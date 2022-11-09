from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    expired_date: Optional[date]


class LoginResponse(BaseModel):
    token: str
    user: User


class Recycle(BaseModel):
    uri: str
    updated_at: datetime
    id: int
