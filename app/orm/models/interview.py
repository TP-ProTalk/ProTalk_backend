from datetime import datetime

from sqlalchemy import Integer, Column, Text, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from app.orm.base import Base


class Interview(Base):
    __tablename__ = 'interviews'

    id = Column(Integer, primary_key=True)
    user_score = Column(Integer, nullable=True)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    vacancy_id = Column(Integer, ForeignKey('vacancies.id'), nullable=False)
    vacancy = relationship("Vacancy", back_populates="interviews")
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="interviews")
    question_associations = relationship("InterviewQuestionAssociation", back_populates="interview")

    def calculate_score(self):
        """Рассчитать итоговый балл за собеседование"""
        if not self.question_associations:
            return 0
        total = sum(q.answer_score for q in self.question_associations if q.answer_score is not None)
        self.user_score = round(total / len(self.question_associations), 1)
        return self.user_score

    def add_question(self, question, answer=None, score=None):
        """Добавить вопрос в собеседование"""
        assoc = InterviewQuestionAssociation(
            interview_id=self.id,
            question_id=question.id,
            answer=answer,
            answer_score=score
        )
        return assoc

    def is_completed(self):
        """Проверить завершено ли собеседование"""
        return self.user_score is not None

    def __repr__(self):
        return f"<Interview(id={self.id}, user_id={self.user_id}, score={self.user_score})>"


class InterviewQuestionAssociation(Base):
    __tablename__ = 'interview_question_associations'

    id = Column(Integer, primary_key=True)
    answer_score = Column(Integer, nullable=True)
    answer = Column(String(255), nullable=True)

    interview_id = Column(Integer, ForeignKey('interviews.id'), nullable=False)
    interview = relationship("Interview", back_populates="question_associations")
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    question = relationship("Question", back_populates="interview_associations")

    def evaluate(self, answer, score=None):
        """Оценить ответ на вопрос"""
        self.answer = answer
        if score is None:
            self.answer_score = 1 if self.question.check_answer(answer) else 0
        else:
            self.answer_score = score
        return self.answer_score

    def __repr__(self):
        return f"<IQA(interview={self.interview_id}, question={self.question_id}, score={self.answer_score})>"


