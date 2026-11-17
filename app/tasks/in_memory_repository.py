from .repository import TaskRepository
from .task import Task

class TaskNotFoundError(Exception):
    pass

class InMemoryTaskRepository(TaskRepository):

    def __init__(self):
        self.tasks: dict[int, Task] = {}

    def save(self, task) -> None:
        self.tasks[task.task_id] = task

    def find_by_id(self, task_id) -> Task:
        if task_id not in self.tasks:
            raise TaskNotFoundError(f"Task with id {task_id} was not found.")

        return self.tasks[task_id]

    def find_all_by_user(self, user_id) -> list[Task]:
        return [
            task
            for task in self.tasks.values()
            if task.owner_id == user_id
        ]

    def update(self, task) -> None:
        if task.task_id not in self.tasks:
            raise TaskNotFoundError(f"Task with id {task.task_id} was not found.")

        self.tasks[task.task_id] = task

    def delete(self, task_id) -> None:
        if task_id not in self.tasks:
            raise TaskNotFoundError(f"Task with id {task_id} was not found.")

        del self.tasks[task_id]