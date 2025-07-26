from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class Todo(BaseModel):
    id: int
    task: str
    done: bool = False

todos: List[Todo] = []
next_id = 1  # ใช้นับ id ของ Todo

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos})

@app.post("/create-todo")
def create_todo(item: str = Form(...)):
    global next_id
    todos.append(Todo(id=next_id, task=item))
    next_id += 1
    return RedirectResponse("/", status_code=303)

@app.post("/todos/{todo_id}/complete")
def complete_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            todo.done = True
            break
    return RedirectResponse("/", status_code=303)

@app.get("/todos/pending", response_class=HTMLResponse)
def get_pending_todos(request: Request):
    pending = [todo for todo in todos if not todo.done]
    return templates.TemplateResponse("pending.html", {"request": request, "todos": pending})

@app.post("/todos/{todo_id}/delete")
def delete_todo(todo_id: int):
    global todos
    todos = [todo for todo in todos if todo.id != todo_id]
    return RedirectResponse("/", status_code=303)

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    pending = [todo for todo in todos if not todo.done]
    return templates.TemplateResponse("index.html", {
        "request": request,
        "todos": todos,
        "pending_todos": pending
    })
