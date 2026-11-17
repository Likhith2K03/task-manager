from datetime import date

class Task:
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

    def __init__(
        self, 
        task_id: int,
        owner_id: int,
        title: str, 
        description: str | None = None, 
        deadline: date | None = None,
    ):
        if not title.strip():
            raise ValueError("Title cannot be empty.")

        if len(title) > 250:
            raise ValueError("Title cannot exceed 250 characters.")

        if deadline is not None and deadline < date.today():
            raise ValueError("Deadline cannot in the past.")


        self.task_id = task_id
        self.owner_id = owner_id
        self.title = title
        self.description = description
        self.deadline = deadline
        self._status = self.PENDING

    @property
    def status(self):
        return self._status

    def start(self):
        if self._status != self.PENDING:
            raise ValueError("Only pending tasks can be started.")

        self._status = self.IN_PROGRESS

    def complete(self):
        if self._status != self.IN_PROGRESS:
            raise ValueError("Only in-progress tasks can be completed.")

        self._status = self.COMPLETED