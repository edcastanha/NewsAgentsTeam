# queue/consumers/proccess_receiver.py

import json
import pika 
from unidecode import unidecode 
from nltk.corpus import stopwords 
from news_app.models import Source 
from core_dj.settings import RABBITMQ_URL, RABBITMQ_QUEUE_NEWS_INCOMING, RABBITMQ_EXCHANGE, RABBITMQ_ROUTING_KEY_CLASSIFICATION # Importações das configurações [4]

# Carregar stop words
nltk.download('stopwords')
stop_words_pt = set(stopwords.words('portuguese'))

def normalize_text(text):
    if not text:
        return ""
    # Remover acentuação, Converter para minúsculas e Remover stop words
    text = unidecode(text)
    text = text.lower()
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words_pt]
    return " ".join(filtered_words)

def callback(ch, method, properties, body):
    try:
        news_data_raw = json.loads(body.decode())
        title = news_data_raw.get('titulo') # Assumindo um campo 'titulo'
        content = news_data_raw.get('conteudo') # Assumindo um campo 'conteudo'


        source = Source.objects.create(raw_data=news_data_raw)

        if not title or not content:
            print(f"Título ou conteúdo ausente na mensagem: {news_data_raw}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False) # Não reenviar se faltar dados essenciais
            raise ValueError("Título ou conteúdo ausente")

        title_normalized = normalize_text(title)
        content_normalized = normalize_text(content)

        # Publicar mensagem para a fila de classificação (conterá o ID da Source)
        publish_classification_task(source.id, title_normalized, content_normalized)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except json.JSONDecodeError:
        print(f"Erro ao decodificar JSON: {body}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True) # Reenviar em caso de erro inesperado

def publish_classification_task(source_id, title_normalized, content_normalized):
    credentials = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(credentials)
    channel = connection.channel()
    channel.exchange_declare(exchange=RABBITMQ_EXCHANGE, exchange_type='direct')
    message = json.dumps({'source_id': source_id, 'title_normalized': title_normalized, 'content_normalized': content_normalized})
    channel.basic_publish(exchange=RABBITMQ_EXCHANGE, routing_key=RABBITMQ_ROUTING_KEY_CLASSIFICATION, body=message)
    connection.close()
    print(f"Mensagem para classificação publicada para Source ID: {source_id}")

if __name__ == '__main__':
    credentials = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(credentials)
    channel = connection.channel()

    channel.exchange_declare(exchange=RABBITMQ_EXCHANGE, exchange_type='direct')
    channel.queue_declare(queue=RABBITMQ_QUEUE_NEWS_INCOMING, durable=True)
    channel.queue_bind(exchange=RABBITMQ_EXCHANGE, queue=RABBITMQ_QUEUE_NEWS_INCOMING, routing_key=RABBITMQ_ROUTING_KEY_INCOMING)

    channel.basic_qos(prefetch_count=1) # Processar uma mensagem por vez
    channel.basic_consume(queue=RABBITMQ_QUEUE_NEWS_INCOMING, on_message_callback=callback)

    print('Aguardando mensagens...')
    channel.start_consuming()
