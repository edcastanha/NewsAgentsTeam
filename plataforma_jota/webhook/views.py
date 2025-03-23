import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status

from queue.publisher import publish_message
from news_app.models import Source
from django.conf import settings

logger = logging.getLogger(__name__)

@csrf_exempt
@require_POST
@api_view(['POST'])
@permission_classes([AllowAny])
def webhook_receiver(request):
    """
    Endpoint para receber notícias via Webhook.
    Recebe dados em formato JSON e os envia para a fila de processamento.
    """
    try:
        data = json.loads(request.body)
        
        # Validação básica dos dados recebidos
        required_fields = ['title', 'content', 'source']
        for field in required_fields:
            if field not in data:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Campo obrigatório ausente: {field}'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Salvar notícia no banco, inicialmente na tabela Source
        receiver = Source.objects.create(
            source=data.get('source'),
            url=data.get('url', ''),
            published_at=data.get('published_at', None),
            raw_data=data,
            is_classified=False
        )
        
        # Publicar mensagem na fila para processamento
        message = {
            'news_id': receiver.id,
            'action': 'process_news'
        }
        
        publish_message(
            message=message,
            exchange=settings.RABBITMQ_EXCHANGE,
            routing_key=settings.RABBITMQ_ROUTING_KEY_INCOMING
        )
        
        logger.info(f"Notícia recebida e enviada para processamento: {news.id}")
        
        return JsonResponse({
            'status': 'success',
            'message': 'Notícia recebida com sucesso',
            'news_id': news.id
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