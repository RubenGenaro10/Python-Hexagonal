from src.application.use_cases.task_manager import TaskManagerUseCase
from src.domain.exceptions import TaskNotFoundError

class TaskCLI:
    """
    Adaptador primario (Driving). Interactúa con el usuario.
    Usa los Casos de Uso para ejecutar la lógica de la aplicación.
    """
    def __init__(self, task_manager: TaskManagerUseCase):
        self.task_manager = task_manager

    def run(self):
        while True:
            print("\n--- Gestor de Tareas (Hexagonal) ---")
            print("1. Crear Tarea")
            print("2. Listar Tareas")
            print("3. Completar Tarea")
            print("4. Salir")
            choice = input("Selecciona una opción: ")
            
            if choice == '1':
                title = input("Título: ")
                desc = input("Descripción: ")
                task = self.task_manager.create_task(title, desc)
                print(f"✅ Tarea creada exitosamente! ID: {task.id}")
            elif choice == '2':
                tasks = self.task_manager.list_tasks()
                if not tasks:
                    print("No se encontraron tareas.")
                for t in tasks:
                    status = "✅ Completada" if t.completed else "❌ Pendiente"
                    print(f"[{status}] {t.id} - {t.title}: {t.description}")
            elif choice == '3':
                task_id = input("ID de la tarea a completar: ")
                try:
                    self.task_manager.complete_task(task_id)
                    print("✅ Tarea marcada como completada!")
                except TaskNotFoundError as e:
                    print(f"⚠️ Error: {e}")
            elif choice == '4':
                print("¡Hasta luego!")
                break
            else:
                print("⚠️ Opción inválida, intenta de nuevo.")
