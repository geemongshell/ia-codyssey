from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Question
from datetime import datetime

router = APIRouter(
    prefix='/question'
)


@router.post('/create')
def create_question(subject: str, content: str, db: Session = Depends(get_db)):
    question = Question(
        subject=subject,
        content=content,
        create_date=datetime.utcnow()
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


@router.get('/list')
def get_question_list(db: Session = Depends(get_db)):
    questions = db.query(Question).all()
    return questions
