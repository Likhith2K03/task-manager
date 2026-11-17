from app.tasks.service import TaskService
from app.tasks.in_memory_repository import InMemoryTaskRepository

repository = InMemoryTaskRepository()
service = TaskService(repository)

task = service.createTask(
    owner_id=101,
    title="Prepare Breakfast"
)

print(len(repository.find_all_by_user(task.owner_id)))

service.start_task(task.task_id, task.owner_id)
print(len(repository.find_all_by_user(task.owner_id)))

service.complete_task(task.task_id, task.owner_id)
print(len(repository.find_all_by_user(task.owner_id)))

service.delete_task(task.task_id, task.owner_id)
print(len(repository.find_all_by_user(task.owner_id)))