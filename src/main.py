from src.infrastructure.adapters.out_db.memory_task_repository import MemoryTaskRepository
from src.application.use_cases.task_manager import TaskManagerUseCase
from src.infrastructure.adapters.in_cli.cli_app import TaskCLI

def main():
    """
    Composition Root / Punto de Entrada.
    Aquí es donde ensamblamos todas las capas. Las dependencias se inyectan desde afuera.
    """
    # 1. Inicializar Adaptadores Secundarios (Driven)
    repository = MemoryTaskRepository()
    
    # 2. Inicializar Capa de Aplicación (Casos de Uso)
    # Inyectamos el repositorio (cumpliendo con la Inversión de Dependencias)
    task_manager = TaskManagerUseCase(repository)
    
    # 3. Inicializar Adaptadores Primarios (Driving)
    cli_app = TaskCLI(task_manager)
    
    # 4. Ejecutar la aplicación
    cli_app.run()

if __name__ == "__main__":
    main()
