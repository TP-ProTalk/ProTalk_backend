from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.security import get_current_user
from app.orm.models import User, Vacancy
from app.api.schemas.vacancy import VacancyCreate, VacancyResponse, VacancyUpdate
from app.services.vacancy import VacancyService
from app.api.dependencies import get_session

router = APIRouter(prefix="/vacancies", tags=["vacancies"])

@router.post("/", response_model=VacancyResponse)
async def create_vacancy(
    vacancy_data: VacancyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    return VacancyService.create_vacancy(db, vacancy_data)

@router.get("/", response_model=List[VacancyResponse])
async def read_vacancies(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session)
):
    return VacancyService.get_vacancies(db, skip=skip, limit=limit)

@router.get("/{vacancy_id}", response_model=VacancyResponse)
async def read_vacancy(
    vacancy_id: int,
    db: Session = Depends(get_session)
):
    return VacancyService.get_vacancy(db, vacancy_id)

@router.put("/{vacancy_id}", response_model=VacancyResponse)
async def update_vacancy(
    vacancy_id: int,
    vacancy_data: VacancyUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    return VacancyService.update_vacancy(db, vacancy_id, vacancy_data)

@router.delete("/{vacancy_id}")
async def delete_vacancy(
    vacancy_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    VacancyService.delete_vacancy(db, vacancy_id)
    return {"message": "Vacancy deleted successfully"}