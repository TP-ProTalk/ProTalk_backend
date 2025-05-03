from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.security import get_current_user
from app.orm.models import User
from app.api.schemas.test import TestCreate, TestResponse, TestUpdate
from app.services.test import TestService
from app.api.dependencies import get_session

router = APIRouter(prefix="/tests", tags=["tests"])

@router.post("/", response_model=TestResponse)
async def create_test(
    test_data: TestCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    return TestService.create_test(db, test_data)

@router.get("/", response_model=List[TestResponse])
async def read_tests(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session)
):
    return TestService.get_tests(db, skip=skip, limit=limit)

@router.get("/{test_id}", response_model=TestResponse)
async def read_test(
    test_id: int,
    db: Session = Depends(get_session)
):
    return TestService.get_test(db, test_id)

@router.put("/{test_id}", response_model=TestResponse)
async def update_test(
    test_id: int,
    test_data: TestUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    return TestService.update_test(db, test_id, test_data)

@router.delete("/{test_id}")
async def delete_test(
    test_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    TestService.delete_test(db, test_id)
    return {"message": "Test deleted successfully"}