import unittest
from unittest.mock import MagicMock, patch
from django.conf import settings
from message_queue.consumer_source import SourceConsumer
from message_queue.interface.rabbitmq.manager import RabbitMQConnectionManager
from message_queue.interface.aws.manager import SQSSNSConnectionManager
from message_queue.consumers.rabbitmq_consumer import RabbitMQConsumer
from message_queue.consumers.sqs_consumer import SQSConsumer
from message_queue.consumers.helpers.process_receiver import NewsProcessor


class TestSourceConsumer(unittest.TestCase):

    @patch.object(RabbitMQConnectionManager, '__init__', return_value=None)
    @patch.object(RabbitMQConsumer, '__init__', return_value=None)
    def test_init_rabbitmq(self, mock_rabbitmq_consumer_init, mock_rabbitmq_connection_manager_init):
        settings.configure(QUEUE_NEWS_INCOMING="test_queue")
        consumer = SourceConsumer(provider="rabbitmq")
        self.assertEqual(consumer.provider, "rabbitmq")
        self.assertIsInstance(consumer.connection_manager, RabbitMQConnectionManager)
        self.assertIsInstance(consumer.news_processor, NewsProcessor)
        self.assertIsInstance(consumer.consumer, RabbitMQConsumer)
        mock_rabbitmq_connection_manager_init.assert_called_once()
        mock_rabbitmq_consumer_init.assert_called_once_with(
            consumer.connection_manager, "test_queue", consumer.news_processor
        )

    @patch.object(SQSSNSConnectionManager, '__init__', return_value=None)
    @patch.object(SQSConsumer, '__init__', return_value=None)
    def test_init_sqs(self, mock_sqs_consumer_init, mock_sqssns_connection_manager_init):
        settings.configure(QUEUE_NEWS_INCOMING="test_queue")
        consumer = SourceConsumer(provider="sqs")
        self.assertEqual(consumer.provider, "sqs")
        self.assertIsInstance(consumer.connection_manager, SQSSNSConnectionManager)
        self.assertIsInstance(consumer.news_processor, NewsProcessor)
        self.assertIsInstance(consumer.consumer, SQSConsumer)
        mock_sqssns_connection_manager_init.assert_called_once_with(
            region_name="sua_regiao",
            aws_access_key_id="sua_access_key",
            aws_secret_access_key="sua_secret_key"
        )
        mock_sqs_consumer_init.assert_called_once_with(
            consumer.connection_manager, "test_queue", consumer.news_processor
        )

    def test_init_invalid_provider(self):
        with self.assertRaises(ValueError) as context:
            SourceConsumer(provider="invalid_provider")
        self.assertEqual(str(context.exception), "Provedor de mensagens desconhecido: invalid_provider")

    @patch.object(RabbitMQConnectionManager, '__init__', return_value=None)
    @patch.object(RabbitMQConsumer, '__init__', return_value=None)
    def test_get_connection_manager_rabbitmq(self, mock_consumer_init, mock_connection_manager_init):
        consumer = SourceConsumer(provider="rabbitmq")
        connection_manager = consumer._get_connection_manager()
        self.assertIsInstance(connection_manager, RabbitMQConnectionManager)
        mock_connection_manager_init.assert_called_once()

    @patch.object(SQSSNSConnectionManager, '__init__', return_value=None)
    @patch.object(SQSConsumer, '__init__', return_value=None)
    def test_get_connection_manager_sqs(self, mock_consumer_init, mock_connection_manager_init):
        consumer = SourceConsumer(provider="sqs")
        connection_manager = consumer._get_connection_manager()
        self.assertIsInstance(connection_manager, SQSSNSConnectionManager)
        mock_connection_manager_init.assert_called_once_with(
            region_name="sua_regiao",
            aws_access_key_id="sua_access_key",
            aws_secret_access_key="sua_secret_key"
        )

    def test_get_connection_manager_invalid_provider(self):
        consumer = SourceConsumer(provider="rabbitmq")
        consumer.provider = "invalid_provider"
        with self.assertRaises(ValueError) as context:
            consumer._get_connection_manager()
        self.assertEqual(str(context.exception), "Provedor de mensagens desconhecido: invalid_provider")

    @patch.object(RabbitMQConnectionManager, '__init__', return_value=None)
    @patch.object(RabbitMQConsumer, '__init__', return_value=None)
    def test_get_consumer_rabbitmq(self, mock_consumer_init, mock_connection_manager_init):
        settings.configure(QUEUE_NEWS_INCOMING="test_queue")
        consumer = SourceConsumer(provider="rabbitmq")
        consumer.connection_manager = MagicMock()
        consumer.news_processor = MagicMock()
        consumer_instance = consumer._get_consumer()
        self.assertIsInstance(consumer_instance, RabbitMQConsumer)
        mock_consumer_init.assert_called_once_with(
            consumer.connection_manager, "test_queue", consumer.news_processor
        )

    @patch.object(SQSSNSConnectionManager, '__init__', return_value=None)
    @patch.object(SQSConsumer, '__init__', return_value=None)
    def test_get_consumer_sqs(self, mock_consumer_init, mock_connection_manager_init):
        settings.configure(QUEUE_NEWS_INCOMING="test_queue")
        consumer = SourceConsumer(provider="sqs")
        consumer.connection_manager = MagicMock()
        consumer.news_processor = MagicMock()
        consumer_instance = consumer._get_consumer()
        self.assertIsInstance(consumer_instance, SQSConsumer)
        mock_consumer_init.assert_called_once_with(
            consumer.connection_manager, "test_queue", consumer.news_processor
        )

    def test_get_consumer_invalid_provider(self):
        consumer = SourceConsumer(provider="rabbitmq")
        consumer.provider = "invalid_provider"
        with self.assertRaises(ValueError) as context:
            consumer._get_consumer()
        self.assertEqual(str(context.exception), "Provedor de mensagens desconhecido: invalid_provider")

    @patch.object(RabbitMQConsumer, 'consume_messages')
    @patch.object(RabbitMQConnectionManager, '__init__', return_value=None)
    @patch.object(RabbitMQConsumer, '__init__', return_value=None)
    def test_start_consuming(self, mock_consumer_init, mock_connection_manager_init, mock_consume_messages):
        consumer = SourceConsumer(provider="rabbitmq")
        consumer.consumer = MagicMock()
        consumer.start_consuming()
        consumer.consumer.consume_messages.assert_called_once()

if __name__ == '__main__':
    unittest.main()
