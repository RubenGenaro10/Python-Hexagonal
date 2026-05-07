import uuid
from typing import List, Optional
from src.domain.task import Task
from src.application.ports.task_repository import TaskRepository

class MySQLTaskRepository(TaskRepository):
    """
    Simulación de un adaptador de base de datos MySQL.
    Para no obligarte a instalar un servidor MySQL ahora mismo, 
    esto simulará la conexión y las consultas SQL mediante prints,
    pero arquitectónicamente funciona exactamente igual que el real.
    """
    def __init__(self):
        print("🔌 Conectando a la base de datos MySQL (Simulación)...")
        # Diccionario interno solo para mantener la app funcionando en esta prueba
        self._db_simulada = {} 
        
    def save(self, task: Task) -> Task:
        if not task.id:
            task.id = str(uuid.uuid4())
        
        # Simulamos la consulta SQL
        print(f"\n🛢️  [MySQL] Ejecutando: INSERT INTO tasks (id, title, desc) VALUES ('{task.id}', '{task.title}', '{task.description}')")
        
        self._db_simulada[task.id] = task
        return task

    def get_by_id(self, task_id: str) -> Optional[Task]:
        print(f"\n🛢️  [MySQL] Ejecutando: SELECT * FROM tasks WHERE id = '{task_id}'")
        return self._db_simulada.get(task_id)

    def list_all(self) -> List[Task]:
        print("\n🛢️  [MySQL] Ejecutando: SELECT * FROM tasks")
        return list(self._db_simulada.values())
