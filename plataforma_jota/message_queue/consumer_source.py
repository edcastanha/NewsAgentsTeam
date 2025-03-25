import logging
from django.conf import settings
from interface.rabbitmq.manager import RabbitMQConnectionManager
from message_queue.interface.aws.manager import SQSSNSConnectionManager
from message_queue.consumers.rabbitmq_consumer import RabbitMQConsumer
from message_queue.consumers.sqs_consumer import SQSConsumer
from message_queue.interface.consumer import MessageProcessor
from message_queue.consumers.helpers.process_receiver import NewsProcessor

logger = logging.getLogger(__name__)

class SourceConsumer:
    def __init__(self, provider="rabbitmq"):
        self.provider = provider
        self.connection_manager = self._get_connection_manager()
        self.news_processor = NewsProcessor()
        self.consumer = self._get_consumer()

    def _get_connection_manager(self):
        if self.provider == "rabbitmq":
            return RabbitMQConnectionManager()
        elif self.provider == "sqs":
            return SQSSNSConnectionManager(
                region_name="sua_regiao",  # Substitua pela sua região
                aws_access_key_id="sua_access_key",  # Substitua pela sua chave de acesso
                aws_secret_access_key="sua_secret_key"  # Substitua pela sua chave secreta
            )
        else:
            raise ValueError(f"Provedor de mensagens desconhecido: {self.provider}")

    def _get_consumer(self):
        if self.provider == "rabbitmq":
            return RabbitMQConsumer(self.connection_manager, settings.QUEUE_NEWS_INCOMING, self.news_processor)
        elif self.provider == "sqs":
            return SQSConsumer(self.connection_manager, settings.QUEUE_NEWS_INCOMING, self.news_processor)
        else:
            raise ValueError(f"Provedor de mensagens desconhecido: {self.provider}")

    def start_consuming(self):
        self.consumer.consume_messages()

if __name__ == '__main__':
    # Escolha o provedor de mensagens (RabbitMQ ou SQS)
    provider = "rabbitmq"  # Ou "sqs"

    source_consumer = SourceConsumer(provider)
    source_consumer.start_consuming()
