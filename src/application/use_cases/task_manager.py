from src.domain.task import Task
from src.domain.exceptions import TaskNotFoundError
from src.application.ports.task_repository import TaskRepository
from src.application.ports.event_publisher import EventPublisher
from typing import List

class TaskManagerUseCase:
    """
    Use Case para gestionar tareas. 
    Aplica la lógica de la aplicación y orquesta el dominio con los puertos.
    """
    # Ahora inyectamos dos dependencias: el repositorio y el publicador de eventos
    def __init__(self, repository: TaskRepository, event_publisher: EventPublisher):
        self.repository = repository
        self.event_publisher = event_publisher

    def create_task(self, title: str, description: str) -> Task:
        task = Task(id=None, title=title, description=description)
        saved_task = self.repository.save(task)
        
        # Disparamos el evento de dominio
        self.event_publisher.publish("TaskCreated", {
            "task_id": saved_task.id,
            "title": saved_task.title
        })
        
        return saved_task

    def get_task(self, task_id: str) -> Task:
        task = self.repository.get_by_id(task_id)
        if not task:
            raise TaskNotFoundError(f"Tarea con ID {task_id} no encontrada")
        return task
        
    def complete_task(self, task_id: str) -> Task:
        task = self.get_task(task_id)
        task.mark_as_completed()
        updated_task = self.repository.save(task)
        
        # Disparamos el evento de dominio
        self.event_publisher.publish("TaskCompleted", {
            "task_id": updated_task.id
        })
        
        return updated_task

    def list_tasks(self) -> List[Task]:
        return self.repository.list_all()
