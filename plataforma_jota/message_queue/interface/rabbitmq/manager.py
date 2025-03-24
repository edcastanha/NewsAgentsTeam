import pika
from django.conf import settings
import logging

from message_queue.interface.connection import MessagingConnectionManager


logger = logging.getLogger(__name__)

class RabbitMQConnectionManager(MessagingConnectionManager):
    """
    Gerencia a conexão com o RabbitMQ.
    """
    def __init__(self):
        super().__init__()

    def get_connection(self):
        """Retorna a conexão com o RabbitMQ."""
        if self._connection is None or self._connection.is_closed:
            self._connect()
        return self._connection

    def get_channel(self):
        """Retorna o canal de comunicação com o RabbitMQ."""
        if self._channel is None or self._channel.is_closed:
            self._connect()
        return self._channel

    def _connect(self):
        """Estabelece a conexão com o RabbitMQ."""
        try:
            parameters = pika.URLParameters(settings.RABBITMQ_URL)
            self._connection = pika.BlockingConnection(parameters)
            self._channel = self._connection.channel()
            logger.info("Conectado ao RabbitMQ")
        except Exception as e:
            logger.error(f"Erro ao conectar ao RabbitMQ: {str(e)}")
            raise

    def close_connection(self):
        """Fecha a conexão com o RabbitMQ se estiver aberta."""
        if self._connection and self._connection.is_open:
            self._connection.close()
            logger.info("Conexão com o RabbitMQ fechada")
