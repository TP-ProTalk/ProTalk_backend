from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    phone_number: Optional[str] = None
    age: Optional[int] = None
    sex: Optional[str] = None
    grade: Optional[str] = None

class UserCreate(UserBase):
    email: EmailStr
    hashed_password: str
    phone_number: str
    age: int
    sex: str
    grade: str

class UserInDB(UserBase):
    id: int
    email_confirmed: bool = False

    class Config:
        orm_mode = True
        from_attributes = True

class UserResponse(UserInDB):
    pass

class UserUpdate(BaseModel):
    phone_number: Optional[str] = None
    age: Optional[int] = None
    sex: Optional[str] = None
    grade: Optional[str] = None
    password: Optional[str] = None