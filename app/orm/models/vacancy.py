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