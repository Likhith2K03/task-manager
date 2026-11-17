from datetime import date

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.tasks.in_memory_repository import InMemoryTaskRepository
from app.tasks.service import TaskService

app = FastAPI()

repository = InMemoryTaskRepository()
task_service = TaskService(repository)

class TaskCreate(BaseModel):
    owner_id: int
    title: str
    description: str | None = None
    deadline: date | None = None

@app.post("/tasks", status_code=201)
def create_task(request: TaskCreate):
    try:
        task = task_service.createTask(
            owner_id=request.owner_id,
            title=request.title,
            description=request.description,
            deadline=request.deadline,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
 
    return {
        "task_id": task.task_id,
        "owner_id": task.owner_id,
        "title": task.title,
        "description": task.description,
        "deadline": task.deadline,
        "status": task.status,
    }

@app.get("/tasks")
def get_tasks(owner_id: int):
    tasks = task_service.repository.find_all_by_user(owner_id)

    return [
        {
            "task_id": task.task_id,
            "owner_id": task.owner_id,
            "title": task.title,
            "description": task.description,
            "deadline": task.deadline,
            "status": task.status,
        }
        for task in tasks
    ]

@app.get("/tasks/{task_id}")
def get_task(task_id: int, owner_id: int):
    try:
        task = task_service._get_owned_task(task_id, owner_id)
    except PermissionError as error:
        raise HTTPException(status_code=403, detail=str(error))
    except Exception as error:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "task_id": task.task_id,
        "owner_id": task.owner_id,
        "title": task.title,
        "description": task.description,
        "deadline": task.deadline,
        "status": task.status,
    }