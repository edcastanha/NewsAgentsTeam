# Serializer Django REST do app news
from rest_framework import serializers
from .models import NewsModel

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsModel
        fields = '__all__'
