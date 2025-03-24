# news_source/views.py (exemplo adaptado)
import json
import logging
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.views import APIView
from message_queue.publisher import Publisher

logger = logging.getLogger(__name__)

class SourceReceiver(APIView):
    @csrf_exempt
    @permission_classes([AllowAny])
    def post(self, request):
        """
        Endpoint para receber notícias via Webhook.
        Recebe dados em formato JSON e os envia para a fila de processamento.

        Valida se o Body temos um JSON
        
        """
        try:
            logger.debug(f"Dados recebidos via webhook: {request.data}")

            if 'noticias' not in request.data or not isinstance(request.data['noticias'], list):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Formato de dados inválido: esperado uma lista de notícias sob a chave "noticias"'
                }, status=status.HTTP_400_BAD_REQUEST)

            for noticia in request.data['noticias']:
                required_fields = ['titulo', 'conteudo']
                for field in required_fields:
                    if field not in noticia:
                        return JsonResponse({
                            'status': 'error',
                            'message': f'Campo obrigatório ausente na notícia: {field}'
                        }, status=status.HTTP_400_BAD_REQUEST)

                # Publicar mensagem na fila para processamento (adaptado para a estrutura da notícia)
                Publisher.publish_message(
                    message=noticia,  # Publica cada notícia individualmente
                    exchange=settings.RABBITMQ_EXCHANGE,
                    routing_key=settings.RABBITMQ_ROUTING_KEY_INCOMING
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