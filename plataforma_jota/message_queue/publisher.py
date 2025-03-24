import json
import logging
import pika
from django.conf import settings

logger = logging.getLogger(__name__)

def get_rabbitmq_connection():
    """
    Estabelece e retorna uma conexão com o RabbitMQ
    """
    try:
        params = pika.URLParameters(settings.RABBITMQ_URL)
        return pika.BlockingConnection(params)
    except Exception as e:
        logger.error(f"Erro ao conectar ao RabbitMQ: {str(e)}")
        raise

def publish_message(message, exchange, routing_key):
    """
    Publica uma mensagem no RabbitMQ
    
    Args:
        message (dict): A mensagem a ser publicada
        exchange (str): O exchange para publicar a mensagem
        routing_key (str): A chave de roteamento para a mensagem
    
    Returns:
        bool: True se a mensagem foi publicada com sucesso, False caso contrário
    """
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        
        # Declarar exchange
        channel.exchange_declare(
            exchange=exchange,
            exchange_type='direct',
            durable=True
        )
        
        # Declarar filas e bindings dependendo da routing_key
        if routing_key == settings.RABBITMQ_ROUTING_KEY_INCOMING:
            queue_name = settings.RABBITMQ_QUEUE_NEWS_INCOMING
        elif routing_key == settings.RABBITMQ_ROUTING_KEY_CLASSIFICATION:
            queue_name = settings.RABBITMQ_QUEUE_NEWS_CLASSIFICATION
        else:
            logger.error(f"Routing key desconhecida: {routing_key}")
            return False
        
        # Declarar fila
        channel.queue_declare(
            queue=queue_name,
            durable=True
        )
        
        # Bind da fila ao exchange
        channel.queue_bind(
            exchange=exchange,
            queue=queue_name,
            routing_key=routing_key
        )
        
        # Publicar mensagem
        channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Mensagem persistente
                content_type='application/json'
            )
        )
        
        logger.info(f"Mensagem publicada em {exchange} com routing_key {routing_key}")
        connection.close()
        return True
        
    except Exception as e:
        logger.exception(f"Erro ao publicar mensagem no RabbitMQ: {str(e)}")
        return False