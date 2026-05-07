from src.domain.task import Task
from src.domain.exceptions import TaskNotFoundError
from src.application.ports.task_repository import TaskRepository
from typing import List

class TaskManagerUseCase:
    """
    Use Case para gestionar tareas. 
    Aplica la lógica de la aplicación y orquesta el dominio con los puertos.
    """
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(self, title: str, description: str) -> Task:
        task = Task(id=None, title=title, description=description)
        return self.repository.save(task)

    def get_task(self, task_id: str) -> Task:
        task = self.repository.get_by_id(task_id)
        if not task:
            raise TaskNotFoundError(f"Tarea con ID {task_id} no encontrada")
        return task
        
    def complete_task(self, task_id: str) -> Task:
        task = self.get_task(task_id)
        task.mark_as_completed()
        return self.repository.save(task)

    def list_tasks(self) -> List[Task]:
        return self.repository.list_all()
