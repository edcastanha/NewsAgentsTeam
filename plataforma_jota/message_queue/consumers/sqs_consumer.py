import logging
import time
import json
from message_queue.interface.consumer import MessageConsumer, MessageProcessor
from message_queue.interface.aws.manager import SQSSNSConnectionManager

logger = logging.getLogger(__name__)

class SQSConsumer(MessageConsumer):
    """
    Consumer de mensagens do SQS.
    """
    def __init__(self, connection_manager: SQSSNSConnectionManager, queue_name: str, message_processor: MessageProcessor):
        super().__init__(connection_manager, queue_name, message_processor)

    def consume_messages(self):
        """Inicia o consumo de mensagens do SQS."""
        sqs_client, _ = self.connection_manager.get_connection()
        queue_url = sqs_client.get_queue_url(QueueName=self.queue_name)['QueueUrl']

        while True:
            try:
                response = sqs_client.receive_message(
                    QueueUrl=queue_url,
                    AttributeNames=['All'],
                    MaxNumberOfMessages=1,
                    WaitTimeSeconds=20  # Long polling
                )

                messages = response.get('Messages', [])
                for message in messages:
                    try:
                        body = json.loads(message['Body'])
                        self.message_processor.process_message(body)
                        sqs_client.delete_message(
                            QueueUrl=queue_url,
                            ReceiptHandle=message['ReceiptHandle']
                        )
                    except json.JSONDecodeError:
                        logger.error(f"Erro ao decodificar JSON: {message['Body']}")
                        # Não deleta a mensagem para tentar processar novamente
                    except Exception as e:
                        logger.exception(f"Erro ao processar mensagem: {e}")
                        # Não deleta a mensagem para tentar processar novamente

            except Exception as e:
                logger.exception(f"Erro ao receber mensagens do SQS: {e}")

            time.sleep(1)  # Pausa entre as tentativas de polling
