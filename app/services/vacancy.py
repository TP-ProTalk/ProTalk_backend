from sqlalchemy.orm import Session
from typing import List
from app.orm.models import Vacancy
from app.api.schemas.vacancy import VacancyCreate, VacancyResponse, VacancyUpdate
from app.exceptions import NotFoundException

class VacancyService:
    @staticmethod
    def create_vacancy(db: Session, vacancy_data: VacancyCreate) -> VacancyResponse:
        vacancy = Vacancy(**vacancy_data.dict())
        db.add(vacancy)
        db.commit()
        db.refresh(vacancy)
        return vacancy

    @staticmethod
    def get_vacancy(db: Session, vacancy_id: int) -> VacancyResponse:
        vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
        if not vacancy:
            raise NotFoundException("Vacancy not found")
        return vacancy

    @staticmethod
    def get_vacancies(db: Session, skip: int = 0, limit: int = 100) -> List[VacancyResponse]:
        return db.query(Vacancy).offset(skip).limit(limit).all()

    @staticmethod
    def update_vacancy(db: Session, vacancy_id: int, vacancy_data: VacancyUpdate) -> VacancyResponse:
        vacancy = VacancyService.get_vacancy(db, vacancy_id)
        for key, value in vacancy_data.dict(exclude_unset=True).items():
            setattr(vacancy, key, value)
        db.commit()
        db.refresh(vacancy)
        return vacancy

    @staticmethod
    def delete_vacancy(db: Session, vacancy_id: int) -> None:
        vacancy = VacancyService.get_vacancy(db, vacancy_id)
        db.delete(vacancy)
        db.commit()