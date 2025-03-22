# news_app/urls.py
from django.urls import path
from .views import NewsListAll, NewsCreateQueue

urlpatterns = [
    path('news/all/', NewsListAll.as_view(), name='news-list-all'),
    path('news/create/', NewsCreateQueue.as_view(), name='news-create'),
]
