import secrets
import smtplib
import string
from datetime import timedelta, datetime
from email.mime.text import MIMEText
from typing import Optional

import jwt
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from app.api.dependencies import get_session
from app.api.main import oauth2_scheme
from app.api.schemas import UserInDB, UserCreate, Token, TokenData
from app.orm import models as orm_models
from app.orm.models import User
from app.settings import api_settings

api_router = APIRouter(
    prefix="/api/"
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def generate_confirmation_token(length=32):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, api_settings.SECRET_KEY, algorithm=api_settings.ALGORITHM)
    return encoded_jwt


async def send_confirmation_email(email_to: str, token: str):
    confirmation_link = f"http://yourapi.com/confirm-email?token={token}"
    message = f"""
    Подтвердите ваш email, перейдя по ссылке:
    {confirmation_link}
    """
    print(f"Sending email to {email_to} with confirmation link: {confirmation_link}")
    # Реальная реализация:
    msg = MIMEText(message)
    msg['Subject'] = 'Подтверждение email'
    msg['From'] = 'noreply@yourapi.com'
    msg['To'] = email_to
    with smtplib.SMTP('smtp.server.com') as server:
        server.send_message(msg)


@api_router.post("/register/", response_model=UserInDB)
async def register(user: UserCreate, session: Session = Depends(get_session)):
    query = select(orm_models.User).where(orm_models.User.email == user.email)
    db_user = session.execute(query)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    confirmation_token = generate_confirmation_token()
    hashed_password = get_password_hash(user.password)

    db_user = orm_models.User(
        email=user.email,
        hashed_password=hashed_password,
        phone_number=user.phone_number,
        age=user.age,
        sex=user.sex,
        email_confirmed=False,
        confirmation_token=confirmation_token
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    await send_confirmation_email(user.email, confirmation_token)

    return db_user


@api_router.get("/confirm-email/")
async def confirm_email(token: str, session: Session = Depends(get_session)):
    query = select(orm_models.User).where(orm_models.User.confirmation_token == token)
    user = session.execute(query).first()
    if not user:
        raise HTTPException(status_code=404, detail="Invalid confirmation token")

    if user.email_confirmed:
        raise HTTPException(status_code=400, detail="Email already confirmed")

    user.email_confirmed = True
    user.confirmation_token = None
    session.commit()

    return {"message": "Email successfully confirmed"}


@api_router.post("/token/", response_model=Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: Session = Depends(get_session)
):
    query = select(orm_models.User).where(orm_models.User.email == form_data.username)
    user = session.execute(query).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.email_confirmed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email not confirmed",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=api_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(get_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = jwt.decode(token, api_settings.SECRET_KEY, algorithms=[api_settings.ALGORITHM])
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    token_data = TokenData(email=email)

    query = select(orm_models.User).where(orm_models.User == token_data.email)
    user = session.execute(query).first()
    if user is None:
        raise credentials_exception
    return user


@api_router.get("/users/me/")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
