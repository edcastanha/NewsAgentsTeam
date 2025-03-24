# news_source/views.py
import json
import logging
from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated 
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication

from message_queue.interface.rabbitmq.manager import RabbitMQConnectionManager
from message_queue.news_publishers import BreakingNewsPublisher

logger = logging.getLogger(__name__)

class SourceReceiver(APIView):
    authentication_classes = [TokenAuthentication]  # Adicionar TokenAuthentication
    permission_classes = [IsAuthenticated]  # Exigir autenticação para acessar

    def post(self, request):
        """
        Endpoint para receber notícias via Webhook (apenas POST).
        Requer um token de autenticação para acesso.
        Recebe dados em formato JSON e os envia para a fila de processamento.

        Valida se o Body temos um JSON

        """
        try:
            logger.debug(f"Dados recebidos via webhook: {request}")

            if 'noticias' not in request.data or not isinstance(request.data['noticias'], list):
                logging.error(f"Dados inválidos recebidos via webhook: {request.data}")
                return JsonResponse({
                    'status': 'error',
                    'message': 'Formato de dados inválido: esperado uma lista de notícias sob a chave "noticias"'
                }, status=status.HTTP_400_BAD_REQUEST)
            # Cria o gerenciador de conexão com o RabbitMQ
            connection_manager = RabbitMQConnectionManager()

            publisher = BreakingNewsPublisher(connection_manager)

            for noticia in request.data['noticias']:
                required_fields = ['titulo', 'conteudo']
                for field in required_fields:
                    if field not in noticia:
                        return JsonResponse({
                            'status': 'error',
                            'message': f'Campo obrigatório ausente na notícia: {field}'
                        }, status=status.HTTP_400_BAD_REQUEST)

                    #TODO: Validar quantidade minima de caracter para conteudo e se Titulo nao é null (???)

                # Publicar mensagem na fila para processamento (adaptado para a estrutura da notícia)
                publisher._publish_rabbitmq_message(
                    message=noticia,
                    exchange=settings.EXCHANGE_NEWS,
                    routing_key=settings.ROUTING_KEY_INCOMING
                )
                logger.info(f"Notícia recebida e enviada para processamento: {noticia}")

            return JsonResponse({
                'status': 'success',
                'message': 'Notícias recebidas e enviadas para processamento com sucesso',
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.exception(f"Erro ao processar webhook: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': f'Erro ao processar webhook: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)