# qwer11/domain/question/question_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Question
from schemas import QuestionRead


router = APIRouter(
    prefix='/api/question'
)


def db_session():
    with get_db() as db:
        yield db


@router.get('/list', response_model=list[QuestionRead])
def question_list(db: Session = Depends(db_session)):
    questions = db.query(Question).all()
    return questions
