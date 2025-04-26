from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.orm.base import Base
from app.orm.models.knowledge import Knowledge


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(Text, nullable=False)
    correct_answer = Column(String(255), nullable=False)

    test_id = Column(Integer, ForeignKey('tests.id'), nullable=False)
    test = relationship("Test", back_populates="questions")
    knowledge_id = Column(Integer, ForeignKey('knowledge.id'), nullable=True)
    knowledge = relationship("Knowledge", back_populates="questions")
    interview_associations = relationship("InterviewQuestionAssociation", back_populates="question")

    def check_answer(self, answer):
        """Проверить правильность ответа"""
        return answer.strip().lower() == self.correct_answer.strip().lower()

    def get_related_knowledge(self):
        """Получить связанные материалы для изучения"""
        return self.knowledge or Knowledge(text="No additional materials", links="")

    def __repr__(self):
        return f"<Question(id={self.id}, text={self.question[:50]}...)>"



class Test(Base):
    __tablename__ = 'tests'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    grade = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)

    vacancy_id = Column(Integer, ForeignKey('vacancies.id'), nullable=False)
    vacancy = relationship("Vacancy", back_populates="tests")
    questions = relationship("Question", back_populates="test")

    def add_question(self, question_text, correct_answer, knowledge=None):
        """Добавить вопрос в тест"""
        question = Question(
            question=question_text,
            correct_answer=correct_answer,
            test_id=self.id,
            knowledge=knowledge
        )
        return question

    def get_random_questions(self, limit=10):
        """Получить случайные вопросы из теста"""
        import random
        return random.sample(self.questions, min(limit, len(self.questions)))

    def __repr__(self):
        return f"<Test(id={self.id}, name={self.name})>"
