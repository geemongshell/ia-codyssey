# model.py
from pydantic import BaseModel

# 각 ToDo 항목의 데이터 구조를 정의하는 모델
class TodoItem(BaseModel):
    id: int
    title: str
    description: str
