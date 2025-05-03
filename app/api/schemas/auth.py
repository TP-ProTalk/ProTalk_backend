from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class TokenPayload(BaseModel):
    sub: str  # subject (обычно email пользователя)
    exp: datetime  # expiration time

    class Config:
        orm_mode = True


class EmailConfirmation(BaseModel):
    message: str
    confirmed_at: Optional[datetime] = None