from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    phone_number: Optional[str] = None
    age: Optional[int] = None
    sex: Optional[str] = None


class UserInDB(UserCreate):
    hashed_password: str
    email_confirmed: bool = False
    confirmation_token: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class EmailConfirmation(BaseModel):
    token: str
