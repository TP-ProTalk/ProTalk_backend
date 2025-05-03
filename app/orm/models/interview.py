from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.orm.base import Base


class Interview(Base):
    __tablename__ = 'interviews'

    id = Column(Integer, primary_key=True)
    user_score = Column(Integer, nullable=True)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    vacancy_id = Column(Integer, ForeignKey('vacancies.id'), nullable=False)
    vacancy = relationship("Vacancy", back_populates="interviews")
    user_associations = relationship("InterviewUserAssociation", back_populates="interview")
    question_associations = relationship("InterviewQuestionAssociation", back_populates="interview")