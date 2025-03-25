import logging
import pika
from message_queue.interface.consumer import MessageConsumer, MessageProcessor
from message_queue.interface.rabbitmq.manager import RabbitMQConnectionManager

logger = logging.getLogger(__name__)

class RabbitMQConsumer(MessageConsumer):
    """
    Consumer de mensagens do RabbitMQ.
    """
    def __init__(self, connection_manager: RabbitMQConnectionManager, queue_name: str, message_processor: MessageProcessor):
        super().__init__(connection_manager, queue_name, message_processor)

    def consume_messages(self):
        """Inicia o consumo de mensagens do RabbitMQ."""
        try:
            channel = self.connection_manager.get_channel()
            channel.queue_declare(queue=self.queue_name, durable=True)
            channel.basic_qos(prefetch_count=1)  # Processar uma mensagem por vez
            channel.basic_consume(queue=self.queue_name, on_message_callback=self._callback)

            logger.info(f"Aguardando mensagens na fila {self.queue_name}...")
            channel.start_consuming()
        except Exception as e:
            logger.exception(f"Erro ao consumir mensagens do RabbitMQ: {e}")
