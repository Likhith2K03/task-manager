import pytest

from app.tasks.task import Task
from app.tasks.service import TaskService
from app.tasks.in_memory_repository import (
    InMemoryTaskRepository,
    TaskNotFoundError,
)


def create_service():
    repository = InMemoryTaskRepository()
    service = TaskService(repository)

    return service, repository


def test_create_task():
    service, repository = create_service()

    task = service.createTask(
        owner_id=101,
        title="Learn backend testing",
    )

    assert task.task_id == 1
    assert task.owner_id == 101
    assert task.title == "Learn backend testing"
    assert task.status == Task.PENDING

    assert repository.find_by_id(1) == task


def test_start_task():
    service, repository = create_service()

    task = service.createTask(
        owner_id=101,
        title="Learn Python",
    )

    result = service.start_task(task.task_id, 101)

    assert result.status == Task.IN_PROGRESS


def test_complete_task():
    service, repository = create_service()

    task = service.createTask(
        owner_id=101,
        title="Learn Python",
    )

    service.start_task(task.task_id, 101)
    result = service.complete_task(task.task_id, 101)

    assert result.status == Task.COMPLETED


def test_user_cannot_start_another_users_task():
    service, repository = create_service()

    task = service.createTask(
        owner_id=101,
        title="Private task",
    )

    with pytest.raises(PermissionError):
        service.start_task(task.task_id, 202)

    assert task.status == Task.PENDING


def test_delete_task():
    service, repository = create_service()

    task = service.createTask(
        owner_id=101,
        title="Task to delete",
    )

    service.delete_task(task.task_id, 101)

    with pytest.raises(TaskNotFoundError):
        repository.find_by_id(task.task_id)


def test_cannot_delete_another_users_task():
    service, repository = create_service()

    task = service.createTask(
        owner_id=101,
        title="Private task",
    )

    with pytest.raises(PermissionError):
        service.delete_task(task.task_id, 202)

    assert repository.find_by_id(task.task_id) == task