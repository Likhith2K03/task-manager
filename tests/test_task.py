from datetime import date

import pytest

from app.tasks.task import Task

def create_task():
    return Task(
        task_id=1,
        owner_id=101,
        title="Learn Python testing",
    )

def test_new_task_starts_as_pending():
    task = create_task()

    assert task.status == Task.PENDING


def test_pending_task_can_be_started():
    task = create_task()

    task.start()

    assert task.status == Task.IN_PROGRESS

def test_pending_task_cannot_be_completed_directly():
    task = create_task()

    with pytest.raises(ValueError):
        task.complete()

    assert task.status == Task.PENDING

def test_in_progress_task_can_be_completed():
    task = create_task()
    task.start()

    task.complete()

    assert task.status == Task.COMPLETED

def test_completed_task_cannot_be_started_again():
    task = create_task()
    task.start()
    task.complete()

    with pytest.raises(ValueError):
        task.start()

    assert task.status == Task.COMPLETED

def test_task_title_cannot_be_empty():
    with pytest.raises(ValueError, match="Title cannot be empty"):
        Task(
        task_id=1,
        owner_id=101,
        title=" ",
        )

def test_task_deadline_cannot_be_in_the_past():
    with pytest.raises(ValueError, match="Deadline cannot"):
        Task(
        task_id=1,
        owner_id=101,
        title="Learn Python testing",
        deadline=date(2000, 1, 1),
        )