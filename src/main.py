from src.infrastructure.adapters.out_db.memory_task_repository import MemoryTaskRepository
from src.infrastructure.adapters.out_db.mysql_task_repository import MySQLTaskRepository
from src.infrastructure.adapters.out_db.mongo_task_repository import MongoTaskRepository
from src.application.use_cases.task_manager import TaskManagerUseCase
from src.infrastructure.adapters.in_cli.cli_app import TaskCLI

def main():
    """
    Composition Root / Punto de Entrada.
    Aquí es donde ensamblamos todas las capas.
    """
    print("="*40)
    print("   SELECCIÓN DE BASE DE DATOS (ADAPTADOR)")
    print("="*40)
    print("1. En Memoria (RAM)")
    print("2. MySQL (Simulado)")
    print("3. MongoDB (Simulado)")
    opcion = input("Elige dónde guardar las tareas (1/2/3): ")

    # 1. Inicializar Adaptadores Secundarios (Driven)
    if opcion == "2":
        repository = MySQLTaskRepository()
    elif opcion == "3":
        repository = MongoTaskRepository()
    else:
        print("🧠 Usando base de datos en Memoria.")
        repository = MemoryTaskRepository()
    
    print("-" * 40)
    
    # 2. Inicializar Capa de Aplicación (Casos de Uso)
    # Aquí probamos la INVERSIÓN DE DEPENDENCIAS:
    # A task_manager no le importa qué 'repository' elegiste arriba. 
    # Mientras cumpla con la interfaz TaskRepository, funcionará perfecto.
    task_manager = TaskManagerUseCase(repository)
    
    # 3. Inicializar Adaptadores Primarios (Driving)
    cli_app = TaskCLI(task_manager)
    
    # 4. Ejecutar la aplicación
    cli_app.run()

if __name__ == "__main__":
    main()
