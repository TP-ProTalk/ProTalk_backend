from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.orm.base import Base


class InterviewUserAssociation(Base):
    __tablename__ = 'interview_user_associations'

    id = Column(Integer, primary_key=True)
    interview_id = Column(Integer, ForeignKey('interviews.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    interview = relationship("Interview", back_populates="user_associations")
    user = relationship("User", back_populates="interview_associations")


class InterviewQuestionAssociation(Base):
    __tablename__ = 'interview_question_associations'

    id = Column(Integer, primary_key=True)
    answer_score = Column(Integer, nullable=True)
    answer = Column(String(255), nullable=True)

    interview_id = Column(Integer, ForeignKey('interviews.id'), nullable=False)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)

    interview = relationship("Interview", back_populates="question_associations")
    question = relationship("Question", back_populates="interview_associations")