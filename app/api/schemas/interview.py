from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class InterviewBase(BaseModel):
    vacancy_id: int
    details: Optional[str] = None

class InterviewCreate(InterviewBase):
    pass

class InterviewResponse(InterviewBase):
    id: int
    user_score: Optional[float] = None
    created_at: datetime
    user_id: int

    class Config:
        orm_mode = True

class InterviewUpdate(BaseModel):
    details: Optional[str] = None
    user_score: Optional[float] = None

class InterviewQuestionAssociationBase(BaseModel):
    question_id: int
    answer: Optional[str] = None
    answer_score: Optional[int] = None

class InterviewQuestionAssociationCreate(InterviewQuestionAssociationBase):
    pass

class InterviewQuestionAssociationResponse(InterviewQuestionAssociationBase):
    id: int
    interview_id: int

    class Config:
        orm_mode = True