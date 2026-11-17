from abc import ABC, abstractmethod

from .task import Task

class TaskRepository(ABC):

    @abstractmethod
    def save(self, task: Task) -> None:
        pass

    @abstractmethod
    def find_by_id(self, task_id: int) -> Task:
        pass

    @abstractmethod
    def find_all_by_user(self, user_id: int) -> list[Task]:
        pass

    @abstractmethod
    def update(self, task: Task) -> None:
        pass

    @abstractmethod
    def delete(self, task_id: int) -> None:
        pass
