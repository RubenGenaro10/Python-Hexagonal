import uuid
from typing import List, Optional
from src.domain.task import Task
from src.application.ports.task_repository import TaskRepository

class MongoTaskRepository(TaskRepository):
    """
    Simulación de un adaptador de base de datos MongoDB (NoSQL).
    Simula la conexión y operaciones usando sintaxis parecida a Mongoose/MongoDB.
    """
    def __init__(self):
        print("🍃 Conectando a MongoDB en mongodb://localhost:27017 (Simulación)...")
        self._collection_simulada = {}
        
    def save(self, task: Task) -> Task:
        if not task.id:
            task.id = str(uuid.uuid4())
            
        print(f"\n🍃 [MongoDB] Ejecutando: db.tasks.insertOne({{_id: '{task.id}', title: '{task.title}', desc: '{task.description}'}})")
        
        self._collection_simulada[task.id] = task
        return task

    def get_by_id(self, task_id: str) -> Optional[Task]:
        print(f"\n🍃 [MongoDB] Ejecutando: db.tasks.findOne({{_id: '{task_id}'}})")
        return self._collection_simulada.get(task_id)

    def list_all(self) -> List[Task]:
        print("\n🍃 [MongoDB] Ejecutando: db.tasks.find({})")
        return list(self._collection_simulada.values())
