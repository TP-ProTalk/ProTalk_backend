from typing import Optional
from pydantic import BaseModel

class VacancyBase(BaseModel):
    name: str
    description: Optional[str] = None

class VacancyCreate(VacancyBase):
    pass

class VacancyResponse(VacancyBase):
    id: int

    class Config:
        orm_mode = True

class VacancyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None