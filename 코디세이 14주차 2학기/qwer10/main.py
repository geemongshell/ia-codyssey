from fastapi import FastAPI
from database import Base, engine
from domain.question import question_router

def create_app():
    Base.metadata.create_all(bind=engine)
    app = FastAPI()
    app.include_router(question_router.router)
    return app


app = create_app()
