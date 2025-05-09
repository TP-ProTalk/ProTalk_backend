from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.security import get_current_user
from app.orm.models import User
from app.api.schemas.question import QuestionCreate, QuestionResponse, QuestionUpdate
from app.services.question import QuestionService
from app.api.dependencies import get_session

router = APIRouter(prefix="/questions", tags=["questions"])

@router.post("/", response_model=QuestionResponse)
async def create_question(
    question_data: QuestionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    return QuestionService.create_question(db, question_data)

@router.get("/", response_model=List[QuestionResponse])
async def read_questions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session)
):
    return QuestionService.get_questions(db, skip=skip, limit=limit)

@router.get("/{question_id}", response_model=QuestionResponse)
async def read_question(
    question_id: int,
    db: Session = Depends(get_session)
):
    return QuestionService.get_question(db, question_id)

@router.put("/{question_id}", response_model=QuestionResponse)
async def update_question(
    question_id: int,
    question_data: QuestionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    return QuestionService.update_question(db, question_id, question_data)

@router.delete("/{question_id}")
async def delete_question(
    question_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    QuestionService.delete_question(db, question_id)
    return {"message": "Question deleted successfully"}

@router.get("/test/{test_id}", response_model=List[QuestionResponse])
async def read_test_questions(
    test_id: int,
    db: Session = Depends(get_session)
):
    return QuestionService.get_questions_by_test(db, test_id)