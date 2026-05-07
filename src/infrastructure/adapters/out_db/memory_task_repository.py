import uuid
from typing import List, Optional, Dict
from src.domain.task import Task
from src.application.ports.task_repository import TaskRepository

class MemoryTaskRepository(TaskRepository):
    """
    Adaptador secundario (Driven). Implementa el puerto TaskRepository.
    Se comunica con un sistema externo (en este caso, una BD en memoria).
    """
    def __init__(self):
        self.tasks: Dict[str, Task] = {}

    def save(self, task: Task) -> Task:
        if not task.id:
            task.id = str(uuid.uuid4())
        self.tasks[task.id] = task
        return task

    def get_by_id(self, task_id: str) -> Optional[Task]:
        return self.tasks.get(task_id)

    def list_all(self) -> List[Task]:
        return list(self.tasks.values())
