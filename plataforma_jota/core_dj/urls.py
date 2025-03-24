from django.contrib import admin
from django.urls import path, include

from .views import GetTokenView

from rest_framework.routers import DefaultRouter

from news_app.views import NewsViewSet, CategoryViewSet
from news_source.views import SourceReceiver

router = DefaultRouter()
# ------ NEWS ---------
router.register(r'api/news', NewsViewSet, basename='news')

# ------ CATEGORY ---------
router.register(r'api/category', CategoryViewSet, basename='category')



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/get-token/', GetTokenView.as_view(), name='get-token'),
    path('api/source/', SourceReceiver.as_view(), name='source-receiver'),

    path('', include(router.urls)),
    
    path('', include('django_prometheus.urls'))
]
