import logging

from .models import NewsModel
from .serializers import NewsSerializer
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import NewsModel as News
from django.core.exceptions import ValidationError


logger = logging.getLogger(__name__)

class NewsCreateQueue(APIView):
    permissions = [permissions.IsAuthenticated,]
    
    def post(self, request):
        try:
            news_data = request.data
            news = News(**news_data)
            news.full_clean()
            news.save()

            return Response({'message': 'News data sent to queue successfully'}, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating news: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class NewsListAll(generics.ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated,]