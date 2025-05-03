from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from app.orm.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    email_confirmed = Column(Boolean, nullable=True, default=True)
    phone_number = Column(String(20), unique=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    confirmation_token = Column(String(255), nullable=True)
    age = Column(Integer, nullable=True)
    sex = Column(String(10), nullable=True)
    grade = Column(String(50), nullable=True)

    vacancy_id = Column(Integer, ForeignKey('vacancies.id'), nullable=True)
    vacancy = relationship("Vacancy", back_populates="users")
    interview_associations = relationship("InterviewUserAssociation", back_populates="user")

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)