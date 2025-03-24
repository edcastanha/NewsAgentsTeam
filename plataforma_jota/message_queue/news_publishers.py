import json
import logging
import pika
from message_queue.interface.rabbitmq.manager import RabbitMQConnectionManager

logger = logging.getLogger(__name__)

class BreakingNewsPublisher:
    """
    Responsável por publicar mensagens no RabbitMQ.
    Utiliza o MessagingConnectionManager para obter a conexão e o canal.
    """
    def __init__(self, connection_manager: RabbitMQConnectionManager):  # Especifica RabbitMQConnectionManager
        if not isinstance(connection_manager, RabbitMQConnectionManager):
            raise TypeError("connection_manager deve ser uma instância de RabbitMQConnectionManager")
        self.connection_manager = connection_manager

    def publish_message(self, message, exchange, routing_key):
        """
        Publica uma mensagem no RabbitMQ.
        Args:
            message (dict): A mensagem a ser publicada.
            exchange (str): O exchange.
            routing_key (str): A chave de roteamento.
        Returns:
            bool: True se a mensagem foi publicada com sucesso, False caso contrário.
        """
        try:
            return self._publish_rabbitmq_message(message, exchange, routing_key)
        except Exception as e:
            logger.exception(f"Erro ao publicar mensagem: {str(e)}")
            return False

    def _publish_rabbitmq_message(self, message, exchange, routing_key):
        """Publica a mensagem no RabbitMQ."""
        try:
            channel = self.connection_manager.get_channel()
            channel.exchange_declare(exchange=exchange, exchange_type='direct', durable=True)
            queue_name = routing_key
            channel.queue_declare(queue=queue_name, durable=True)
            channel.queue_bind(exchange=exchange, queue=queue_name, routing_key=routing_key)
            channel.basic_publish(
                exchange=exchange,
                routing_key=routing_key,
                body=json.dumps(message, ensure_ascii=False), 
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Mensagem persistente
                    content_type='application/json'
                )
            )
            logger.info(f"Mensagem publicada no RabbitMQ. Exchange: {exchange}, Routing Key: {routing_key}")
            return True
        except Exception as e:
            logger.exception(f"Erro ao publicar mensagem no RabbitMQ: {str(e)}")
            return False
