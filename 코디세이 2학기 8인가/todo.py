# todo.py
# Python 3.x 버전 사용
# FastAPI + uvicorn 기반
# 별도의 DB 없이 메모리 내 리스트(todo_list) 사용
# PEP 8 스타일 및 지정된 코딩 규칙 준수

from fastapi import FastAPI, APIRouter
from typing import Dict, List

# FastAPI 인스턴스 생성
app = FastAPI()

# APIRouter 인스턴스 생성
router = APIRouter()

# todo_list 리스트 객체 생성
todo_list: List[Dict[str, str]] = []


@router.post('/add_todo')
def add_todo(item: Dict[str, str]) -> Dict[str, str]:
    """
    새로운 할 일을 todo_list에 추가.
    요청 방식: POST
    입력: {"task": "할 일 내용"}
    출력: {"message": "추가 완료", "task": "할 일 내용"}
    """
    if 'task' not in item:
        return {'error': 'task 키가 필요합니다.'}
    todo_list.append({'task': item['task']})
    return {'message': 'TODO 항목이 추가되었습니다.', 'task': item['task']}


@router.get('/retrieve_todo')
def retrieve_todo() -> Dict[str, List[Dict[str, str]]]:
    """
    현재 저장된 todo_list를 반환함.
    요청 방식: GET
    출력: {"todo_list": [{"task": "예시1"}, {"task": "예시2"}]}
    """
    return {'todo_list': todo_list}


# APIRouter를 FastAPI 앱에 등록
app.include_router(router)
