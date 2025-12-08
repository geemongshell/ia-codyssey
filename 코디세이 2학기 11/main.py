# qwer11/main.py
from fastapi import FastAPI

from database import Base, engine
from domain.question.question_router import router as question_router


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(question_router)
