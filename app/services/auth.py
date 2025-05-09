from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.api.schemas import UserInDB
from app.core.security import (
    create_access_token,
    verify_password,
    get_password_hash,
    generate_confirmation_token
)
from app.orm.models import User
from app.services.email import send_confirmation_email


class AuthService:
    @staticmethod
    def register_user(db: Session, user_data):
        # Проверка существования пользователя
        with db as session:
            if session.query(User).filter(User.email == user_data.email).first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )

            # Создание пользователя
            hashed_password = get_password_hash(user_data.password)
            confirmation_token = generate_confirmation_token()

            user = User(
                email=user_data.email,
                hashed_password=hashed_password,
                phone_number=user_data.phone_number,
                age=user_data.age,
                sex=user_data.sex,
                confirmation_token=confirmation_token
            )

            session.add(user)
            session.commit()
            session.refresh(user)

            # Отправка email
            send_confirmation_email(user.email, confirmation_token)

            return UserInDB.model_validate(user)

    @staticmethod
    def authenticate_user(db: Session, form_data):
        with db as session:
            user = session.query(User).filter(User.email == form_data.username).first()
            if not user or not verify_password(form_data.password, user.hashed_password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect email or hashed_password"
                )
            if not user.email_confirmed:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Email not confirmed"
                )

            access_token = create_access_token(
                user.email,
                expires_delta=timedelta(minutes=30)
            )

            return {"access_token": access_token, "token_type": "bearer"}

    @staticmethod
    def confirm_email(db: Session, token: str):
        user = db.query(User).filter(User.confirmation_token == token).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid confirmation token"
            )

        user.email_confirmed = True
        user.confirmation_token = None
        db.commit()

        return {"message": "Email successfully confirmed"}