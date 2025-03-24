import json
import logging
import pika
import time

from django.conf import settings
from news_app.models import News

from classifier.services.category_classifier import CategoryClassifier

logger = logging.getLogger(__name__)

# Instanciar classificadores
category_classifier = CategoryClassifier()


def callback(ch, method, properties, body):
    """
    Callback para processar mensagens da fila de classificação.
    
    Args:
        ch: Canal RabbitMQ
        method: Método da mensagem
        properties: Propriedades da mensagem
        body: Corpo da mensagem
    """
    try:
        message = json.loads(body)
        logger.info(f"Mensagem de classificação recebida: {message}")
        
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
            
        # Classificar notícia
        try:
            # Classificar categoria
            category, subcategory, confidence = category_classifier.classify_category(
                news.title, news.content
            )
            
            
            # Atualizar notícia
            news.category = category
            news.subcategory = subcategory
            news.is_classified = True
            
            # Armazenar dados de classificação
            news.classification_data = {
                'category_confidence': confidence,
                'classification_timestamp': time.time(),
                'tags_count': len(tags)
            }
            
            # Salvar notícia
            news.save()
            
            # Associar tags
            news.tags.set(tags)
            
            logger.info(f"Notícia {news_id} classificada com sucesso: categoria={category}, urgente={is_urgent}, tags={len(tags)}")
            
        except Exception as e:
            logger.exception(f"Erro ao classificar notícia {news_id}: {str(e)}")
            # Mesmo com erro, marcamos como processada para não ficar em loop
            news.is_classified = True
            news.classification_data = {
                'error': str(e),
                'classification_timestamp': time.time()
            }
            news.save()
        
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
    Inicia o consumidor para a fila de classificação de notícias
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
                queue=settings.RABBITMQ_QUEUE_NEWS_CLASSIFICATION,
                durable=True
            )
            
            # Binding da fila ao exchange
            channel.queue_bind(
                exchange=settings.RABBITMQ_EXCHANGE,
                queue=settings.RABBITMQ_QUEUE_NEWS_CLASSIFICATION,
                routing_key=settings.RABBITMQ_ROUTING_KEY_CLASSIFICATION
            )
            
            # Configurar QoS (Quality of Service)
            channel.basic_qos(prefetch_count=1)
            
            # Configurar consumidor
            channel.basic_consume(
                queue=settings.RABBITMQ_QUEUE_NEWS_CLASSIFICATION,
                on_message_callback=callback
            )
            
            logger.info('Consumidor de classificação iniciado. Aguardando mensagens...')
            channel.start_consuming()
            
        except pika.exceptions.AMQPConnectionError:
            retry_count += 1
            wait_time = 5 * retry_count  # Backoff exponencial
            logger.error(f"Falha na conexão com RabbitMQ. Tentativa {retry_count} de {max_retries}. Aguardando {wait_time} segundos...")
            time.sleep(wait_time)
            
        except KeyboardInterrupt:
            logger.info("Consumidor de classificação interrompido manualmente")
            if 'connection' in locals() and connection.is_open:
                connection.close()
            break
            
        except Exception as e:
            logger.exception(f"Erro no consumidor de classificação: {str(e)}")
            if 'connection' in locals() and connection.is_open:
                connection.close()
            time.sleep(5)
            retry_count += 1
            
    logger.error("Número máximo de tentativas de conexão excedido. Encerrando consumidor de classificação.")

if __name__ == "__main__":
    start_consumer()