import unittest
import json
from unittest.mock import MagicMock, patch
from message_queue.news_publishers import BreakingNewsPublisher
from message_queue.interface.rabbitmq.manager import RabbitMQConnectionManager
import pika

class TestBreakingNewsPublisher(unittest.TestCase):

    def setUp(self):
        self.mock_connection_manager = MagicMock(spec=RabbitMQConnectionManager)
        self.mock_channel = MagicMock()
        self.mock_connection_manager.get_channel.return_value = self.mock_channel
        self.publisher = BreakingNewsPublisher(self.mock_connection_manager)
        self.message = {"key": "value"}
        self.exchange = "test_exchange"
        self.routing_key = "test_routing_key"

    def test_init_with_invalid_connection_manager(self):
        with self.assertRaises(TypeError):
            BreakingNewsPublisher(MagicMock())

    def test_publish_message_success(self):
        result = self.publisher.publish_message(self.message, self.exchange, self.routing_key)
        self.assertTrue(result)
        self.mock_connection_manager.get_channel.assert_called_once()
        self.mock_channel.exchange_declare.assert_called_once_with(
            exchange=self.exchange, exchange_type='direct', durable=True
        )
        self.mock_channel.queue_declare.assert_called_once_with(
            queue=self.routing_key, durable=True
        )
        self.mock_channel.queue_bind.assert_called_once_with(
            exchange=self.exchange, queue=self.routing_key, routing_key=self.routing_key
        )
        self.mock_channel.basic_publish.assert_called_once_with(
            exchange=self.exchange,
            routing_key=self.routing_key,
            body=json.dumps(self.message, ensure_ascii=False),
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type='application/json'
            )
        )

    def test_publish_message_failure(self):
        self.mock_channel.basic_publish.side_effect = Exception("Publish failed")
        result = self.publisher.publish_message(self.message, self.exchange, self.routing_key)
        self.assertFalse(result)
        self.mock_connection_manager.get_channel.assert_called_once()
        self.mock_channel.exchange_declare.assert_called_once_with(
            exchange=self.exchange, exchange_type='direct', durable=True
        )
        self.mock_channel.queue_declare.assert_called_once_with(
            queue=self.routing_key, durable=True
        )
        self.mock_channel.queue_bind.assert_called_once_with(
            exchange=self.exchange, queue=self.routing_key, routing_key=self.routing_key
        )
        self.mock_channel.basic_publish.assert_called_once_with(
            exchange=self.exchange,
            routing_key=self.routing_key,
            body=json.dumps(self.message, ensure_ascii=False),
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type='application/json'
            )
        )

    def test_publish_rabbitmq_message_success(self):
        result = self.publisher._publish_rabbitmq_message(self.message, self.exchange, self.routing_key)
        self.assertTrue(result)
        self.mock_connection_manager.get_channel.assert_called_once()
        self.mock_channel.exchange_declare.assert_called_once_with(
            exchange=self.exchange, exchange_type='direct', durable=True
        )
        self.mock_channel.queue_declare.assert_called_once_with(
            queue=self.routing_key, durable=True
        )
        self.mock_channel.queue_bind.assert_called_once_with(
            exchange=self.exchange, queue=self.routing_key, routing_key=self.routing_key
        )
        self.mock_channel.basic_publish.assert_called_once_with(
            exchange=self.exchange,
            routing_key=self.routing_key,
            body=json.dumps(self.message, ensure_ascii=False),
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type='application/json'
            )
        )

    def test_publish_rabbitmq_message_failure(self):
        self.mock_channel.basic_publish.side_effect = Exception("Publish failed")
        result = self.publisher._publish_rabbitmq_message(self.message, self.exchange, self.routing_key)
        self.assertFalse(result)
        self.mock_connection_manager.get_channel.assert_called_once()
        self.mock_channel.exchange_declare.assert_called_once_with(
            exchange=self.exchange, exchange_type='direct', durable=True
        )
        self.mock_channel.queue_declare.assert_called_once_with(
            queue=self.routing_key, durable=True
        )
        self.mock_channel.queue_bind.assert_called_once_with(
            exchange=self.exchange, queue=self.routing_key, routing_key=self.routing_key
        )
        self.mock_channel.basic_publish.assert_called_once_with(
            exchange=self.exchange,
            routing_key=self.routing_key,
            body=json.dumps(self.message, ensure_ascii=False),
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type='application/json'
            )
        )

if __name__ == '__main__':
    unittest.main()
