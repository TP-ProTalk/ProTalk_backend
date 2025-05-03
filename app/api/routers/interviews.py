from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.orm.models import User
from app.api.schemas.interview import (
    InterviewCreate,
    InterviewResponse,
    InterviewUpdate,
    InterviewQuestionAssociationCreate,
    InterviewQuestionAssociationResponse
)
from app.services.interview import InterviewService
from app.api.dependencies import get_session

router = APIRouter(prefix="/interviews", tags=["interviews"])

@router.post("/", response_model=InterviewResponse)
async def create_interview(
    interview_data: InterviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    return InterviewService.create_interview(db, current_user.id, interview_data)

@router.get("/{interview_id}", response_model=InterviewResponse)
async def get_interview(
    interview_id: int,
    db: Session = Depends(get_session)
):
    return InterviewService.get_interview(db, interview_id)

@router.patch("/{interview_id}", response_model=InterviewResponse)
async def update_interview(
    interview_id: int,
    update_data: InterviewUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    return InterviewService.update_interview(db, interview_id, current_user.id, update_data)

@router.delete("/{interview_id}")
async def delete_interview(
    interview_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    InterviewService.delete_interview(db, interview_id, current_user.id)
    return {"message": "Interview deleted successfully"}

@router.get("/user/me", response_model=list[InterviewResponse])
async def get_my_interviews(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100
):
    return InterviewService.get_user_interviews(db, current_user.id, skip, limit)

@router.post("/{interview_id}/questions", response_model=InterviewQuestionAssociationResponse)
async def add_question_to_interview(
    interview_id: int,
    question_data: InterviewQuestionAssociationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    return InterviewService.add_question_to_interview(db, interview_id, current_user.id, question_data)

@router.post("/questions/{association_id}/evaluate", response_model=InterviewQuestionAssociationResponse)
async def evaluate_question(
    association_id: int,
    score: int,
    answer: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    return InterviewService.evaluate_interview_question(db, association_id, current_user.id, score, answer)