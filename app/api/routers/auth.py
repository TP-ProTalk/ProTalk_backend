from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.schemas.auth import Token, EmailConfirmation
from app.api.schemas.user import UserCreate, UserInDB
from app.services.auth import AuthService
from app.api.dependencies import get_session

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserInDB)
async def register(user: UserCreate, db: Session = Depends(get_session)):
    return AuthService.register_user(db, user)

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session)
):
    return AuthService.authenticate_user(db, form_data)

@router.get("/confirm-email", response_model=EmailConfirmation)
async def confirm_email(token: str, db: Session = Depends(get_session)):
    return AuthService.confirm_email(db, token)