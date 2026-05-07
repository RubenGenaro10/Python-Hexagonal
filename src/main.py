from src.infrastructure.adapters.out_db.memory_task_repository import MemoryTaskRepository
from src.infrastructure.adapters.out_db.mysql_task_repository import MySQLTaskRepository
from src.infrastructure.adapters.out_db.mongo_task_repository import MongoTaskRepository
from src.infrastructure.adapters.out_event.console_event_publisher import ConsoleEventPublisher
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

    # 1. Inicializar Adaptador de Base de Datos
    if opcion == "2":
        repository = MySQLTaskRepository()
    elif opcion == "3":
        repository = MongoTaskRepository()
    else:
        print("🧠 Usando base de datos en Memoria.")
        repository = MemoryTaskRepository()
        
    # 2. Inicializar Adaptador de Eventos
    event_publisher = ConsoleEventPublisher()
    
    print("-" * 40)
    
    # 3. Inicializar Capa de Aplicación (Casos de Uso)
    # INVERSIÓN DE DEPENDENCIAS: El caso de uso recibe tanto la base de datos 
    # como el sistema de eventos por interfaz, sin importar la implementación.
    task_manager = TaskManagerUseCase(
        repository=repository, 
        event_publisher=event_publisher
    )
    
    # 4. Inicializar Adaptadores Primarios (Driving)
    cli_app = TaskCLI(task_manager)
    
    # 5. Ejecutar la aplicación
    cli_app.run()

if __name__ == "__main__":
    main()
