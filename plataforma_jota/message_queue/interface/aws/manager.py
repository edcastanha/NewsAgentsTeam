import boto3
import logging
from django.conf import settings

from message_queue.interface.connection import MessagingConnectionManager

logger = logging.getLogger(__name__)

class SQSSNSConnectionManager(MessagingConnectionManager):
    """
    Gerencia a conexão com o SQS e SNS da AWS.
    """
    def __init__(self):
        super().__init__()
        self.sqs_client = boto3.client('sqs', region_name=settings.AWS_REGION)
        self.sns_client = boto3.client('sns', region_name=settings.AWS_REGION)

    def get_connection(self):
        """Retorna a conexão SQS ou SNS (não persistente, mas segue o contrato)."""
        # No caso do SQS/SNS, a conexão é stateless, então, não precisamos de uma conexão persistente
        return self.sqs_client, self.sns_client

    def get_channel(self):
        """Retorna um canal lógico de comunicação (SQS/SNS não têm canal, então retornamos a conexão)."""
        return self.get_connection()

    def close_connection(self):
        """Como o SQS/SNS são sem estado, não há necessidade de fechar a conexão explicitamente."""
        logger.info("Conexão com o SQS/SNS não precisa ser fechada explicitamente.")
