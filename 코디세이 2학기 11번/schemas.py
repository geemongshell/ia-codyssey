# qwer11/schemas.py
from pydantic import BaseModel
from datetime import datetime


class QuestionRead(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime

    class Config:
        from_attributes = True
