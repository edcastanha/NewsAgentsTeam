import json
import logging
import pika
import time
import django
import os

# Configurar Django para execução como script
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_dj.settings')
django.setup()

from django.conf import settings
from queue.publisher import publish_message
from news.models import News

logger = logging.getLogger(__name__)

def callback(ch, method, properties, body):
    """
    Callback para processar mensagens recebidas da fila de notícias.
    
    Args:
        ch: Canal RabbitMQ
        method: Método da mensagem
        properties: Propriedades da mensagem
        body: Corpo da mensagem
    """
    try:
        message = json.loads(body)
        logger.info(f"Mensagem recebida: {message}")
        
        news_id = message.get('news_id')
        if not news_id:
            logger.error("ID da notícia não encontrado na mensagem")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
            
        # Buscar notícia no banco
        try:
            news = News.objects.get(id=news_id)
        except News.DoesNotExist:
            logger.error(f"Notícia com ID {news_id} não encontrada")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
            
        # Marcar notícia como processada
        news.is_processed = True
        news.save(update_fields=['is_processed'])
        
        # Encaminhar para classificação
        classification_message = {
            'news_id': news.id,
            'action': 'classify_news'
        }
        
        publish_result = publish_message(
            message=classification_message,
            exchange=settings.RABBITMQ_EXCHANGE,
            routing_key=settings.RABBITMQ_ROUTING_KEY_CLASSIFICATION
        )
        
        if publish_result:
            logger.info(f"Notícia {news_id} encaminhada para classificação")
        else:
            logger.error(f"Erro ao encaminhar notícia {news_id} para classificação")
        
        # Confirmar processamento da mensagem
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except json.JSONDecodeError:
        logger.error("Erro ao decodificar mensagem JSON")
        # Mesmo com erro, confirmamos recebimento para não processar repetidamente
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except Exception as e:
        logger.exception(f"Erro ao processar mensagem: {str(e)}")
        # Em caso de erro, devolvemos a mensagem para a fila após um delay
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def start_consumer():
    """
    Inicia o consumidor para a fila de recebimento de notícias
    """
    # Número de tentativas de conexão
    max_retries = 5
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # Estabelecer conexão com RabbitMQ
            params = pika.URLParameters(settings.RABBITMQ_URL)
            connection = pika.BlockingConnection(params)
            channel = connection.channel()
            
            # Declarar exchange
            channel.exchange_declare(
                exchange=settings.RABBITMQ_EXCHANGE,
                exchange_type='direct',
                durable=True
            )
            
            # Declarar fila
            channel.queue_declare(
                queue=settings.RABBITMQ_QUEUE_NEWS_INCOMING,
                durable=True
            )
            
            # Binding da fila ao exchange
            channel.queue_bind(
                exchange=settings.RABBITMQ_EXCHANGE,
                queue=settings.RABBITMQ_QUEUE_NEWS_INCOMING,
                routing_key=settings.RABBITMQ_ROUTING_KEY_INCOMING
            )
            
            # Configurar QoS (Quality of Service)
            channel.basic_qos(prefetch_count=1)
            
            # Configurar consumidor
            channel.basic_consume(
                queue=settings.RABBITMQ_QUEUE_NEWS_INCOMING,
                on_message_callback=callback
            )
            
            logger.info('Consumidor de recebimento iniciado. Aguardando mensagens...')
            channel.start_consuming()
            
        except pika.exceptions.AMQPConnectionError:
            retry_count += 1
            wait_time = 5 * retry_count  # Backoff exponencial
            logger.error(f"Falha na conexão com RabbitMQ. Tentativa {retry_count} de {max_retries}. Aguardando {wait_time} segundos...")
            time.sleep(wait_time)
            
        except KeyboardInterrupt:
            logger.info("Consumidor de recebimento interrompido manualmente")
            if 'connection' in locals() and connection.is_open:
                connection.close()
            break
            
        except Exception as e:
            logger.exception(f"Erro no consumidor de recebimento: {str(e)}")
            if 'connection' in locals() and connection.is_open:
                connection.close()
            time.sleep(5)
            retry_count += 1
            
    logger.error("Número máximo de tentativas de conexão excedido. Encerrando consumidor de recebimento.")

if __name__ == "__main__":
    start_consumer()