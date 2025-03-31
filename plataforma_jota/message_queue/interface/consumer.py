import abc
import json
import logging
from message_queue.interface.connection import MessagingConnectionManager

logger = logging.getLogger(__name__)

class MessageProcessor(abc.ABC):
    @abc.abstractmethod
    def process_message(self, message):
        pass

class MessageConsumer(abc.ABC):
    """
    Interface abstrata para consumers de mensagens.
    """
    def __init__(self, connection_manager: MessagingConnectionManager, queue_name: str, message_processor: MessageProcessor):
        self.connection_manager = connection_manager
        self.queue_name = queue_name
        self.message_processor = message_processor

    @abc.abstractmethod
    def consume_messages(self):
        """Inicia o consumo de mensagens."""
        pass

    def _callback(self, ch, method, properties, body):
        """Callback genérico para processar mensagens."""
        try:
            message = json.loads(body.decode())
            logger.debug(f" ----- --------- Mensagem recebida: --------- ----- :: /n {message}")
            self.message_processor.process_message(message)
            ch.basic_ack(delivery_tag=method.delivery_tag)  # Confirma o recebimento
        except json.JSONDecodeError:
            logger.error(f"Erro ao decodificar JSON: {body}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)  # Não reenfileira se for erro de JSON
        except Exception as e:
            logger.exception(f"Erro ao processar mensagem: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)  # Reenfileira em caso de erro
