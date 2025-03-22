from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from .models import NewsModel
from datetime import datetime

class NewsAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.news_data = {
            'fonte': 'Teste Fonte',
            'url': 'http://teste.com',
            'titulo': 'Teste Título',
            'conteudo': 'Teste Conteúdo',
            'data_publicacao': datetime.now(),
            'autor': 'Teste Autor',
            'categoria_original': 'Teste Categoria',
            'tags': ['tag1', 'tag2'],
            'informacoes_adicionais': {'chave': 'valor'}
        }
        self.news = NewsModel.objects.create(**self.news_data)

    def test_create_news(self):
        url = reverse('news-list')
        response = self.client.post(url, self.news_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NewsModel.objects.count(), 2)
        # Retrieve the newly created news object (excluding the one created in setUp)
        created_news = NewsModel.objects.exclude(id=self.news.id).first()
        self.assertIsNotNone(created_news, "The created NewsModel instance should exist.")
        # Assert each field in self.news_data matches the created_news field
        for field, expected_value in self.news_data.items():
            self.assertEqual(getattr(created_news, field), expected_value, f"Field '{field}' does not match.")

    def test_get_news_list(self):
        url = reverse('news-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_news_detail(self):
        url = reverse('news-detail', args=[self.news.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['titulo'], self.news_data['titulo'])

    def test_update_news(self):
        url = reverse('news-detail', args=[self.news.id])
        updated_data = self.news_data.copy()
        updated_data['titulo'] = 'Título Atualizado'
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        