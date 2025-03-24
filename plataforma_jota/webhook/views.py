import json
import logging
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.views import APIView

from message_queue.publisher import publish_message

logger = logging.getLogger(__name__)

class SourceReceiver(APIView):

    @csrf_exempt
    @api_view(['POST'])
    @permission_classes([AllowAny])
    def post(self, request):
        """
        Endpoint para receber notícias via Webhook.
        Recebe dados em formato JSON e os envia para a fila de processamento.
        """
        
        try:
            data_source = json.loads(request.body)
            
            # Validação básica dos dados recebidos
            required_fields = ['title', 'content']
            for field in required_fields:
                if field not in data_source:
                    return JsonResponse({
                        'status': 'error',
                        'message': f'Campo obrigatório ausente: {field}'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Publicar mensagem na fila para processamento
            publish_message(
                message=request.body,
                exchange=settings.RABBITMQ_EXCHANGE,
                routing_key=settings.RABBITMQ_ROUTING_KEY_INCOMING
            )
            
            logger.info(f"Notícia recebida e enviada para processamento")
            
            return JsonResponse({
                'status': 'success',
                'message': 'Notícia recebida com sucesso',
            }, status=status.HTTP_201_CREATED)
            
        except json.JSONDecodeError:
            logger.error("Erro ao decodificar JSON do webhook")
            return JsonResponse({
                'status': 'error',
                'message': 'Formato JSON inválido'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.exception(f"Erro ao processar webhook: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': f'Erro ao processar webhook: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)