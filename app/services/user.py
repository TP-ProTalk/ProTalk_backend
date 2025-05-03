from sqlalchemy.orm import Session
from typing import List, Optional
from app.orm.models import User
from app.api.schemas.user import UserCreate, UserUpdate, UserResponse
from app.core.security import get_password_hash
from app.exceptions import NotFoundException, ConflictException


class UserService:
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> UserResponse:
        """Получение пользователя по ID"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundException("User not found")
        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[UserResponse]:
        """Получение пользователя по email"""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> UserResponse:
        """Создание нового пользователя"""
        # Проверка на существующего пользователя
        if UserService.get_user_by_email(db, user_data.email):
            raise ConflictException("Email already registered")

        hashed_password = get_password_hash(user_data.hashed_password)
        user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            phone_number=user_data.phone_number,
            age=user_data.age,
            sex=user_data.sex,
            grade=user_data.grade
        )

        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update_user(
            db: Session,
            user_id: int,
            update_data: UserUpdate
    ) -> UserResponse:
        """Обновление данных пользователя"""
        user = UserService.get_user_by_id(db, user_id)

        if update_data.phone_number is not None:
            user.phone_number = update_data.phone_number
        if update_data.age is not None:
            user.age = update_data.age
        if update_data.sex is not None:
            user.sex = update_data.sex
        if update_data.grade is not None:
            user.grade = update_data.grade
        if update_data.password is not None:
            user.hashed_password = get_password_hash(update_data.password)

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_users(
            db: Session,
            skip: int = 0,
            limit: int = 100
    ) -> List[UserResponse]:
        """Получение списка пользователей"""
        return db.query(User).offset(skip).limit(limit).all()