from sqlalchemy import Column, Integer, Text, String
from sqlalchemy.orm import relationship

from app.orm.base import Base
from app.orm.models.test import Question


class Knowledge(Base):
    __tablename__ = 'knowledge'

    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    links = Column(String(255), nullable=True)

    questions = relationship("Question", back_populates="knowledge")

    def add_question(self, question_text, correct_answer, test):
        """Создать вопрос с привязкой к этому материалу"""
        return Question(
            question=question_text,
            correct_answer=correct_answer,
            test=test,
            knowledge=self
        )

    def __repr__(self):
        return f"<Knowledge(id={self.id}, text={self.text[:50]}...)>"