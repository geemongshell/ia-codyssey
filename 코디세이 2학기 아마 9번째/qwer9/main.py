# main.py
from fastapi import FastAPI, HTTPException
from model import TodoItem
import csv

app = FastAPI()
csv_file = 'todo.csv'


# CSV 파일에서 모든 항목을 읽어오는 함수
def read_todos():
    todos = []
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                todos.append({
                    'id': int(row['id']),
                    'title': row['title'],
                    'description': row['description']
                })
    except FileNotFoundError:
        with open(csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['id', 'title', 'description'])
            writer.writeheader()
    return todos


# CSV 파일에 항목을 저장하는 함수
def write_todos(todos):
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'title', 'description'])
        writer.writeheader()
        for todo in todos:
            writer.writerow(todo)


@app.get('/todos')
def get_all_todos():
    todos = read_todos()
    return {'todos': todos}


@app.get('/todos/{todo_id}')
def get_single_todo(todo_id: int):
    todos = read_todos()
    for todo in todos:
        if todo['id'] == todo_id:
            return todo
    raise HTTPException(status_code=404, detail='Todo not found')


@app.post('/todos')
def add_todo(item: TodoItem):
    todos = read_todos()
    for todo in todos:
        if todo['id'] == item.id:
            raise HTTPException(status_code=400, detail='Todo ID already exists')
    todos.append(item.dict())
    write_todos(todos)
    return {'message': 'Todo added successfully'}


@app.put('/todos/{todo_id}')
def update_todo(todo_id: int, item: TodoItem):
    todos = read_todos()
    for i, todo in enumerate(todos):
        if todo['id'] == todo_id:
            todos[i] = item.dict()
            write_todos(todos)
            return {'message': 'Todo updated successfully'}
    raise HTTPException(status_code=404, detail='Todo not found')


@app.delete('/todos/{todo_id}')
def delete_single_todo(todo_id: int):
    todos = read_todos()
    for i, todo in enumerate(todos):
        if todo['id'] == todo_id:
            del todos[i]
            write_todos(todos)
            return {'message': 'Todo deleted successfully'}
    raise HTTPException(status_code=404, detail='Todo not found')
