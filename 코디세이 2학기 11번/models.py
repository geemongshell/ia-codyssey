# qwer11/models.py
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from database import Base


class Question(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, nullable=False)
    content = Column(String, nullable=False)
    create_date = Column(DateTime, default=datetime.utcnow)
