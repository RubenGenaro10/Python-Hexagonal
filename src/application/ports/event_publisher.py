from abc import ABC, abstractmethod

class EventPublisher(ABC):
    """
    Puerto (Puerto Secundario/Salida) para publicar eventos de dominio.
    El Caso de Uso no necesita saber SI usamos RabbitMQ, Kafka, 
    o simplemente imprimimos en consola.
    """
    @abstractmethod
    def publish(self, event_name: str, payload: dict):
        pass
