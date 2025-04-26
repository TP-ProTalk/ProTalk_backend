from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(20), unique=True, nullable=True)
    password = Column(String(255), nullable=False)
    age = Column(Integer, nullable=True)
    sex = Column(String(10), nullable=True)
    grade = Column(String(50), nullable=True)

    vacancy_id = Column(Integer, ForeignKey('vacancies.id'), nullable=True)
    vacancy = relationship("Vacancy", back_populates="users")
    interviews = relationship("Interview", back_populates="user")

    def set_password(self, password):
        """Хеширование пароля"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Проверка пароля"""
        return check_password_hash(self.password, password)

    def get_active_interviews(self):
        """Получить активные собеседования пользователя"""
        return [i for i in self.interviews if i.user_score is None]

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"



