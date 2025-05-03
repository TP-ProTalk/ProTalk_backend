from sqlalchemy.orm import Session
from typing import List, Optional
from app.orm.models import Test, Vacancy
from app.api.schemas.test import TestCreate, TestUpdate, TestResponse
from app.exceptions import NotFoundException, ConflictException


class TestService:
    @staticmethod
    def create_test(db: Session, test_data: TestCreate) -> TestResponse:
        """Создание нового теста"""
        # Проверяем существование вакансии
        vacancy = db.query(Vacancy).filter(Vacancy.id == test_data.vacancy_id).first()
        if not vacancy:
            raise NotFoundException("Vacancy not found")

        test = Test(**test_data.dict())
        db.add(test)
        db.commit()
        db.refresh(test)
        return test

    @staticmethod
    def get_test(db: Session, test_id: int) -> TestResponse:
        """Получение теста по ID"""
        test = db.query(Test).filter(Test.id == test_id).first()
        if not test:
            raise NotFoundException("Test not found")
        return test

    @staticmethod
    def get_tests(db: Session, skip: int = 0, limit: int = 100) -> List[TestResponse]:
        """Получение списка тестов"""
        return db.query(Test).offset(skip).limit(limit).all()

    @staticmethod
    def update_test(
            db: Session,
            test_id: int,
            test_data: TestUpdate
    ) -> TestResponse:
        """Обновление теста"""
        test = TestService.get_test(db, test_id)
        for field, value in test_data.dict(exclude_unset=True).items():
            setattr(test, field, value)
        db.commit()
        db.refresh(test)
        return test

    @staticmethod
    def delete_test(db: Session, test_id: int) -> None:
        """Удаление теста"""
        test = TestService.get_test(db, test_id)
        db.delete(test)
        db.commit()