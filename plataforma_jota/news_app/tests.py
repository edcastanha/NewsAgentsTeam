from django.test import TestCase
from django.urls import reverse
from rest_framework import status, authtoken
from rest_framework.test import APITestCase
from .models import News, Category, Subcategory, Tag
from .serializers import NewsSerializer, CategorySerializer

class NewsAppTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category", description="Test Description", slug="test-category")
        self.subcategory = Subcategory.objects.create(name="Test Subcategory", description="Test Subcategory Description", slug="test-subcategory", category=self.category)
        self.tag = Tag.objects.create(name="Test Tag", slug="test-tag")
        self.news = News.objects.create(title="Test News", content="Test Content", category=self.category, subcategory=self.subcategory)
        self.news.tags.add(self.tag)
        # Criando user e token para autenticacao
        from django.contrib.auth.models import User
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = authtoken.models.Token.objects.create(user=self.user)  

    def test_news_creation(self):
        self.assertEqual(News.objects.count(), 1)
        self.assertEqual(self.news.title, "Test News")
        self.assertEqual(self.news.category, self.category)
        self.assertEqual(self.news.subcategory, self.subcategory)
        self.assertIn(self.tag, self.news.tags.all())

    def test_category_creation(self):
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(self.category.name, "Test Category")

    def test_subcategory_creation(self):
        self.assertEqual(Subcategory.objects.count(), 1)
        self.assertEqual(self.subcategory.name, "Test Subcategory")
        self.assertEqual(self.subcategory.category, self.category)

    def test_tag_creation(self):
        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(self.tag.name, "Test Tag")

    def test_news_list_api(self):
        url = reverse('news-list')  # Use the correct URL name
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(url)        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = NewsSerializer(News.objects.all(), many=True)
        self.assertEqual(response.data, serializer.data)
    
    def test_category_list_api(self):
        url = reverse('category-list')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = CategorySerializer(Category.objects.all(), many=True)
        # Acessando os resultados dentro de 'results'
        self.assertEqual(response.data['results'], serializer.data)
