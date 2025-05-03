from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session

from app.orm.models import Interview, InterviewQuestionAssociation, User, Vacancy, Question
from app.api.schemas.interview import (
    InterviewCreate,
    InterviewResponse,
    InterviewUpdate,
    InterviewQuestionAssociationCreate,
    InterviewQuestionAssociationResponse
)
from app.exceptions import NotFoundException, ForbiddenException


class InterviewService:
    @staticmethod
    def create_interview(
            db: Session,
            user_id: int,
            interview_data: InterviewCreate
    ) -> InterviewResponse:
        """Создание нового собеседования"""
        # Проверяем существование вакансии
        vacancy = db.query(Vacancy).filter(Vacancy.id == interview_data.vacancy_id).first()
        if not vacancy:
            raise NotFoundException("Vacancy not found")

        # Создаем собеседование
        interview = Interview(
            vacancy_id=interview_data.vacancy_id,
            user_id=user_id,
            details=interview_data.details,
            created_at=datetime.utcnow()
        )

        db.add(interview)
        db.commit()
        db.refresh(interview)

        return interview

    @staticmethod
    def get_interview(db: Session, interview_id: int) -> InterviewResponse:
        """Получение собеседования по ID"""
        interview = db.query(Interview).filter(Interview.id == interview_id).first()
        if not interview:
            raise NotFoundException("Interview not found")
        return interview

    @staticmethod
    def update_interview(
            db: Session,
            interview_id: int,
            user_id: int,
            update_data: InterviewUpdate
    ) -> InterviewResponse:
        """Обновление данных собеседования"""
        interview = db.query(Interview).filter(Interview.id == interview_id).first()
        if not interview:
            raise NotFoundException("Interview not found")

        # Проверяем, что пользователь имеет доступ
        if interview.user_id != user_id:
            raise ForbiddenException()

        # Обновляем поля
        if update_data.details is not None:
            interview.details = update_data.details
        if update_data.user_score is not None:
            interview.user_score = update_data.user_score

        db.commit()
        db.refresh(interview)
        return interview

    @staticmethod
    def delete_interview(db: Session, interview_id: int, user_id: int) -> None:
        """Удаление собеседования"""
        interview = db.query(Interview).filter(Interview.id == interview_id).first()
        if not interview:
            raise NotFoundException("Interview not found")

        if interview.user_id != user_id:
            raise ForbiddenException()

        db.delete(interview)
        db.commit()

    @staticmethod
    def get_user_interviews(
            db: Session,
            user_id: int,
            skip: int = 0,
            limit: int = 100
    ) -> List[InterviewResponse]:
        """Получение списка собеседований пользователя"""
        return (
            db.query(Interview)
            .filter(Interview.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def add_question_to_interview(
            db: Session,
            interview_id: int,
            user_id: int,
            question_data: InterviewQuestionAssociationCreate
    ) -> InterviewQuestionAssociationResponse:
        """Добавление вопроса к собеседованию"""
        # Проверяем существование собеседования
        interview = db.query(Interview).filter(Interview.id == interview_id).first()
        if not interview:
            raise NotFoundException("Interview not found")

        # Проверяем права доступа
        if interview.user_id != user_id:
            raise ForbiddenException()

        # Проверяем существование вопроса
        question = db.query(Question).filter(Question.id == question_data.question_id).first()
        if not question:
            raise NotFoundException("Question not found")

        # Создаем связь
        association = InterviewQuestionAssociation(
            interview_id=interview_id,
            question_id=question_data.question_id,
            answer=question_data.answer,
            answer_score=question_data.answer_score
        )

        db.add(association)
        db.commit()
        db.refresh(association)

        return association

    @staticmethod
    def evaluate_interview_question(
            db: Session,
            association_id: int,
            user_id: int,
            score: int,
            answer: Optional[str] = None
    ) -> InterviewQuestionAssociationResponse:
        """Оценка ответа на вопрос собеседования"""
        association = (
            db.query(InterviewQuestionAssociation)
            .filter(InterviewQuestionAssociation.id == association_id)
            .first()
        )

        if not association:
            raise NotFoundException("Question association not found")

        # Проверяем права доступа
        if association.interview.user_id != user_id:
            raise ForbiddenException()

        # Обновляем оценку и ответ
        if answer is not None:
            association.answer = answer
        association.answer_score = score

        db.commit()
        db.refresh(association)

        # Пересчитываем общий балл собеседования
        InterviewService._recalculate_interview_score(db, association.interview_id)

        return association

    @staticmethod
    def _recalculate_interview_score(db: Session, interview_id: int) -> None:
        """Пересчет общего балла собеседования"""
        interview = db.query(Interview).filter(Interview.id == interview_id).first()
        if not interview:
            return

        # Получаем все оценки вопросов
        scores = [
            assoc.answer_score
            for assoc in interview.question_associations
            if assoc.answer_score is not None
        ]

        if scores:
            # Рассчитываем средний балл
            interview.user_score = sum(scores) / len(scores)
            db.commit()