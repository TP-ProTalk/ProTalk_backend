from sqlalchemy.orm import Session
from typing import List, Optional
from app.orm.models import Question, Test
from app.api.schemas.question import QuestionCreate, QuestionUpdate, QuestionResponse
from app.exceptions import NotFoundException, ConflictException


class QuestionService:
    @staticmethod
    def create_question(db: Session, question_data: QuestionCreate) -> QuestionResponse:
        """Создание нового вопроса"""
        with db as session:
            test = session.query(Test).filter(Test.id == question_data.test_id).first()
            if not test:
                raise NotFoundException("Test not found")

            question = Question(**question_data.dict())
            session.add(question)
            session.commit()
            session.refresh(question)
            return question

    @staticmethod
    def get_question(db: Session, question_id: int) -> QuestionResponse:
        """Получение вопроса по ID"""
        question = db.query(Question).filter(Question.id == question_id).first()
        if not question:
            raise NotFoundException("Question not found")
        return question

    @staticmethod
    def get_questions(db: Session, skip: int = 0, limit: int = 100) -> List[QuestionResponse]:
        """Получение списка вопросов"""
        return db.query(Question).offset(skip).limit(limit).all()

    @staticmethod
    def get_questions_by_test(db: Session, test_id: int) -> List[QuestionResponse]:
        """Получение вопросов для конкретного теста"""
        return db.query(Question).filter(Question.test_id == test_id).all()

    @staticmethod
    def update_question(
            db: Session,
            question_id: int,
            question_data: QuestionUpdate
    ) -> QuestionResponse:
        """Обновление вопроса"""
        question = QuestionService.get_question(db, question_id)
        for field, value in question_data.dict(exclude_unset=True).items():
            setattr(question, field, value)
        db.commit()
        db.refresh(question)
        return question

    @staticmethod
    def delete_question(db: Session, question_id: int) -> None:
        """Удаление вопроса"""
        question = QuestionService.get_question(db, question_id)
        db.delete(question)
        db.commit()