from datetime import date

from .repository import TaskRepository
from .task import Task

class TaskService:

    def __init__(self, repository: TaskRepository):
        self.repository = repository
        self.next_id = 1

    def createTask(
            self,
            owner_id: int,
            title: str,
            description: str | None = None,
            deadline: date | None = None
    ) -> Task:
        task = Task (
            task_id=self.next_id,
            owner_id=owner_id,
            title=title,
            description=description,
            deadline=deadline
        )

        self.next_id += 1
        self.repository.save(task)
        return task

    def _get_owned_task(self, task_id: int, owner_id: int) -> Task:
        task = self.repository.find_by_id(task_id)
        
        if task.owner_id != owner_id:
            raise PermissionError("You do not own this task.")

        return task

    def start_task(self, task_id: int, owner_id: int) -> Task:
        task = self._get_owned_task(task_id, owner_id)       
        task.start()
        self.repository.update(task)
        return task

    def complete_task(self, task_id: int, owner_id: int) -> Task:
        task = self._get_owned_task(task_id, owner_id)  
        task.complete()
        self.repository.update(task)        
        return task

    def delete_task(self, task_id: int, owner_id: int) -> None:
        task = self._get_owned_task(task_id, owner_id)  
        self.repository.delete(task_id) 