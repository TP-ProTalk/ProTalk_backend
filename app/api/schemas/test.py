from typing import Optional
from pydantic import BaseModel

class TestBase(BaseModel):
    name: str
    vacancy_id: int
    grade: Optional[str] = None
    description: Optional[str] = None

class TestCreate(TestBase):
    pass

class TestResponse(TestBase):
    id: int

    class Config:
        orm_mode = True

class TestUpdate(BaseModel):
    name: Optional[str] = None
    grade: Optional[str] = None
    description: Optional[str] = None