from .models import NewsModel
from rest_framework import routers, serializers, viewsets



class NewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NewsModel
        fields = ['url', 'fonte', 'url', 'titulo', 'conteudo', 'data_publicacao', 'autor', 'categoria_original', 'tags', 'informacoes_adicionais']

# ViewSets define the view behavior.
class NewsViewSet(viewsets.ModelViewSet):
    queryset = NewsModel.objects.all()
    serializer_class = NewsSerializer

router = routers.DefaultRouter()
router.register(r'news', NewsViewSet)