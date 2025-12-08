# main.py
from fastapi import FastAPI
from domain.question.question_router import router as question_router
from database import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(question_router)
