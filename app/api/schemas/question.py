from typing import Optional
from pydantic import BaseModel

class QuestionBase(BaseModel):
    question: str
    test_id: int
    correct_answer: str
    knowledge_id: Optional[int] = None

class QuestionCreate(QuestionBase):
    pass

class QuestionResponse(QuestionBase):
    id: int

    class Config:
        orm_mode = True

class QuestionUpdate(BaseModel):
    question: Optional[str] = None
    correct_answer: Optional[str] = None
    knowledge_id: Optional[int] = None