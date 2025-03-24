import json
import logging
from message_queue.interface.connection import MessagingConnectionManager
from message_queue.interface.rabbitmq.manager import RabbitMQConnectionManager
from message_queue.interface.aws.manager import SQSSNSConnectionManager


logger = logging.getLogger(__name__)

class Publisher:
    """
    Responsável por publicar mensagens no RabbitMQ, SQS ou SNS.
    Utiliza o MessagingConnectionManager para obter a conexão e o canal.
    """
    def __init__(self, connection_manager: MessagingConnectionManager):
        self.connection_manager = connection_manager

    def publish_message(self, message, exchange, routing_key):
        """
        Publica uma mensagem no RabbitMQ ou SQS/SNS.
        Args:
            message (dict): A mensagem a ser publicada.
            exchange (str): O exchange ou tópico.
            routing_key (str): A chave de roteamento ou nome da fila.
        Returns:
            bool: True se a mensagem foi publicada com sucesso, False caso contrário.
        """
        try:
            # Caso esteja usando RabbitMQ
            if isinstance(self.connection_manager, RabbitMQConnectionManager):
                return self._publish_rabbitmq_message(message, exchange, routing_key)

            # Caso esteja usando SQS/SNS
            elif isinstance(self.connection_manager, SQSSNSConnectionManager):
                return self._publish_sqs_sns_message(message, exchange, routing_key)

            else:
                logger.error(f"Tipo de conexão desconhecido: {type(self.connection_manager)}")
                return False

        except Exception as e:
            logger.exception(f"Erro ao publicar mensagem: {str(e)}")
            return False

    def _publish_rabbitmq_message(self, message, exchange, routing_key):
        """Publica a mensagem no RabbitMQ."""
        channel = self.connection_manager.get_channel()
        channel.exchange_declare(exchange=exchange, exchange_type='direct', durable=True)
        queue_name = routing_key  # Defina conforme sua lógica
        channel.queue_declare(queue=queue_name, durable=True)
        channel.queue_bind(exchange=exchange, queue=queue_name, routing_key=routing_key)
        channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Mensagem persistente
                content_type='application/json'
            )
        )
        logger.info(f"Mensagem publicada no RabbitMQ. Exchange: {exchange}, Routing Key: {routing_key}")
        return True

    def _publish_sqs_sns_message(self, message, queue_name, topic_name):
        """Publica a mensagem no SQS ou SNS."""
        sqs_client, sns_client = self.connection_manager.get_connection()

        if queue_name:  # Se for SQS
            try:
                queue_url = sqs_client.get_queue_url(QueueName=queue_name)['QueueUrl']
                sqs_client.send_message(QueueUrl=queue_url, MessageBody=json.dumps(message))
                logger.info(f"Mensagem publicada na fila SQS: {queue_name}")
                return True
            except Exception as e:
                logger.error(f"Erro ao publicar mensagem no SQS: {str(e)}")
                return False

        elif topic_name:  # Se for SNS
            try:
                topic_arn = sns_client.create_topic(Name=topic_name)['TopicArn']
                sns_client.publish(TopicArn=topic_arn, Message=json.dumps(message))
                logger.info(f"Mensagem publicada no tópico SNS: {topic_name}")
                return True
            except Exception as e:
                logger.error(f"Erro ao publicar mensagem no SNS: {str(e)}")
                return False
        else:
            logger.error("Nenhum nome de fila ou tópico fornecido para o SQS/SNS.")
            return False
