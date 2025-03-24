from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny 
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from .models import News, Category
from .serializers import NewsSerializer, CategorySerializer
from .filters import NewsFilter


# --------- Notícias (News) ------------

class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para gerenciar as notícias.
    """
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]
    filterset_class = NewsFilter


# --------- Categorias (Category) ------------

class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet para listar todas as categorias.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
