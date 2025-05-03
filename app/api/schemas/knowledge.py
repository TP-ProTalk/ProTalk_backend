from typing import Optional
from pydantic import BaseModel

class KnowledgeBase(BaseModel):
    text: str
    links: Optional[str] = None

class KnowledgeCreate(KnowledgeBase):
    pass

class KnowledgeResponse(KnowledgeBase):
    id: int

    class Config:
        orm_mode = True

class KnowledgeUpdate(BaseModel):
    text: Optional[str] = None
    links: Optional[str] = None