from src.application.ports.event_publisher import EventPublisher

class ConsoleEventPublisher(EventPublisher):
    """
    Adaptador Secundario (Driven) que simula el envío de eventos a un 
    Message Broker (como RabbitMQ o Kafka) o servicios externos (como un 
    servicio de Email).
    """
    def publish(self, event_name: str, payload: dict):
        print(f"\n📢 [EVENT BUS] Evento Disparado: '{event_name}'")
        print(f"   ↳ Datos del evento: {payload}")
        
        # Simulamos una reacción asíncrona a un evento
        if event_name == "TaskCompleted":
            print(f"   ↳ 📧 Simulando envío de Email: '¡Felicidades! La tarea {payload.get('task_id')} se completó.'")
