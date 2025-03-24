import django_filters
from .models import News

class NewsFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    published_at = django_filters.DateFilter(field_name='published_at', lookup_expr='date')

    class Meta:
        model = News
        fields = ['title', 'category', 'published_at']