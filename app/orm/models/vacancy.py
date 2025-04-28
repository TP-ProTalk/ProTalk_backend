from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.orm.base import Base


class Vacancy(Base):
    __tablename__ = 'vacancies'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    users = relationship("User", back_populates="vacancy")
    tests = relationship("Test", back_populates="vacancy")
    interviews = relationship("Interview", back_populates="vacancy")

    def get_questions_count(self):
        """Общее количество вопросов по всем тестам вакансии"""
        return sum(len(test.questions) for test in self.tests)

    def get_tests_by_grade(self, grade):
        """Получить тесты для определенного уровня"""
        return [test for test in self.tests if test.grade == grade]

    def __repr__(self):
        return f"<Vacancy(id={self.id}, name={self.name})>"
