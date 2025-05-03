from sqlalchemy import Column, Integer, Text, String, ForeignKey
from sqlalchemy.orm import relationship

from app.orm.base import Base


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