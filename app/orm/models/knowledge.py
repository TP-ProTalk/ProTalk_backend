from sqlalchemy import Column, Integer, Text, String
from sqlalchemy.orm import relationship

from app.orm.base import Base


class Knowledge(Base):
    __tablename__ = 'knowledge'

    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    links = Column(String(255), nullable=True)

    questions = relationship("Question", back_populates="knowledge")