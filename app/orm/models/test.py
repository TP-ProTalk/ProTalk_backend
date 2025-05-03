from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.orm.base import Base


class Test(Base):
    __tablename__ = 'tests'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    grade = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)

    vacancy_id = Column(Integer, ForeignKey('vacancies.id'), nullable=False)
    vacancy = relationship("Vacancy", back_populates="tests")
    questions = relationship("Question", back_populates="test", cascade="all, delete-orphan")