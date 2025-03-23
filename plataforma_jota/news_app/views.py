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

class NewsViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar as notícias.
    """
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = NewsFilter

    def list(self, request, *args, **kwargs):
        """
        Lista todas as notícias, aplicando filtros se fornecidos.
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        """
        Recupera uma notícia específica pelo ID.
        """
        news = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(news)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def filter_queryset(self, queryset):
        """
        Filtra o queryset fornecido com base nos parâmetros GET da solicitação.

        Args:
            queryset (QuerySet): O queryset inicial a ser filtrado.

        Returns:
            QuerySet: O queryset filtrado.

        Raises:
            ValidationError: Se o conjunto de filtros não for válido.
        """
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
        if not filterset.is_valid():
            raise ValidationError(filterset.errors)
        return filterset.qs


# --------- Categorias (Category) ------------

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para listar todas as categorias.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
