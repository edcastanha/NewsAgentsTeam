# message_queue/consumers/helpers/process_receiver.py
import json
import logging
from unidecode import unidecode
import nltk
from django.conf import settings
from news_app.models import Source

from message_queue.interface.consumer import MessageProcessor
from message_queue.news_publishers import BreakingNewsPublisher

from .stopwords import preprocess_text 



logger = logging.getLogger(__name__)


class NewsProcessor(MessageProcessor):
    def __init__(self, publisher: BreakingNewsPublisher):  # Recebe o Publisher no construtor
        self.publisher = publisher

    def process_message(self, message):
        try:
            news_data_raw = message
            news_id = news_data_raw.get('news_id')
            title = news_data_raw.get('titulo')  # Assumindo um campo 'titulo'
            content = news_data_raw.get('conteudo')  # Assumindo um campo 'conteudo'


            if not title or not content:
                logger.error(f"Título ou conteúdo ausente na mensagem: {news_data_raw}")
                raise ValueError("Título ou conteúdo ausente")

            title_normalized = self.normalize_text(title)
            content_normalized = self.normalize_text(content)
            #criar json com registro de source e campos titulo e conteudo normalizados



            # Publicar mensagem para a fila de classificação (conterá o ID da Source)
            self.publish_classification_task(source.id, title_normalized, content_normalized)

        except json.JSONDecodeError:
            logger.error(f"Erro ao decodificar JSON: {message}")
        except Exception as e:
            logger.exception(f"Erro ao processar mensagem: {e}")

    def normalize_text(self, text):
        if not text:
            return ""
        # Remover acentuação, Converter para minúsculas e Remover stop words
        text = preprocess_text(text)
        text = unidecode(text)
        text = text.lower()
        words = text.split()

        logger.debug(words)
        return " ".join(words)

    def publish_classification_task(self, news_id, title_normalized, content_normalized):
        message = json.dumps({'source_id': news_id, 'title_normalized': title_normalized, 'content_normalized': content_normalized})
        success = self.publisher.publish_message(
            message=message,
            exchange=settings.EXCHANGE_NEWS,
            routing_key=settings.ROUTING_KEY_CLASSIFICATION
        )
        if success:
            logger.info(f"Mensagem para classificação publicada para Source ID: {news_id}")
            return True
        else:
            logger.error(f"Erro ao publicar mensagem para classificação para Source ID: {news_id}")
            return False
