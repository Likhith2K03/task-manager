import pytest

from app.tasks.task import Task
from app.tasks.in_memory_repository import (
    InMemoryTaskRepository,
    TaskNotFoundError,
)


def create_task(task_id=1, owner_id=101, title="Learn Python"):
    return Task(
        task_id=task_id,
        owner_id=owner_id,
        title=title,
    )


def test_save_and_find_task():
    repository = InMemoryTaskRepository()
    task = create_task()

    repository.save(task)

    result = repository.find_by_id(1)

    assert result == task


def test_find_all_tasks_by_owner():
    repository = InMemoryTaskRepository()

    task1 = create_task(task_id=1, owner_id=101)
    task2 = create_task(task_id=2, owner_id=101)
    task3 = create_task(task_id=3, owner_id=202)

    repository.save(task1)
    repository.save(task2)
    repository.save(task3)

    result = repository.find_all_by_user(101)

    assert len(result) == 2
    assert task1 in result
    assert task2 in result
    assert task3 not in result


def test_find_nonexistent_task():
    repository = InMemoryTaskRepository()

    with pytest.raises(TaskNotFoundError):
        repository.find_by_id(999)


def test_update_task():
    repository = InMemoryTaskRepository()

    original_task = create_task()
    repository.save(original_task)

    updated_task = create_task(title="Learn Java")

    repository.update(updated_task)

    result = repository.find_by_id(1)

    assert result.title == "Learn Java"


def test_update_nonexistent_task():
    repository = InMemoryTaskRepository()

    task = create_task(task_id=999)

    with pytest.raises(TaskNotFoundError):
        repository.update(task)


def test_delete_task():
    repository = InMemoryTaskRepository()

    task = create_task()
    repository.save(task)

    repository.delete(1)

    with pytest.raises(TaskNotFoundError):
        repository.find_by_id(1)


def test_delete_nonexistent_task():
    repository = InMemoryTaskRepository()

    with pytest.raises(TaskNotFoundError):
        repository.delete(999)