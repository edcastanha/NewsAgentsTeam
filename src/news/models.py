from django.db import models
from django.contrib.postgres.fields import ArrayField
from utils.baseModel import BaseModel

class News(BaseModel):
    fonte = models.CharField(max_length=255, verbose_name="Fonte")
    url = models.URLField(blank=True, null=True, verbose_name="URL")
    titulo = models.CharField(max_length=255, verbose_name="Título")
    conteudo = models.TextField(verbose_name="Conteúdo")
    data_publicacao = models.DateTimeField(verbose_name="Data de Publicação")
    autor = models.CharField(max_length=255, blank=True, null=True, verbose_name="Autor")
    categoria_original = models.CharField(max_length=100, blank=True, null=True, verbose_name="Categoria Original")
    tags = ArrayField(models.CharField(max_length=50), blank=True, null=True, verbose_name="Tags")
    informacoes_adicionais = models.JSONField(blank=True, null=True, verbose_name="Informações Adicionais")

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Notícia"
        verbose_name_plural = "Notícias"
        ordering = ['-data_publicacao'] # Ordena as notícias pela data de publicação mais recente por padrão