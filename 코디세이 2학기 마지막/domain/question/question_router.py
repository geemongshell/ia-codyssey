from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Question
from schemas import QuestionRead, QuestionCreate

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


@router.post('/create', response_model=QuestionRead)
def question_create(question: QuestionCreate, db: Session = Depends(db_session)):
    new_question = Question(subject=question.subject, content=question.content)
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question
