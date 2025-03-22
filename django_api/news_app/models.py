from django.db import models
from django.contrib.postgres.fields import ArrayField
from core.utils.baseModel import BaseModel

class NewsModel(BaseModel):
    fonte = models.CharField(null=True, blank=True,max_length=255, verbose_name="Fonte")
    url = models.URLField(blank=True, null=True, verbose_name="URL")
    titulo = models.CharField(max_length=255, verbose_name="Título")
    conteudo = models.TextField(verbose_name="Conteúdo")
    data_publicacao = models.DateTimeField(verbose_name="Data de Publicação")
    autor = models.CharField(max_length=255, blank=True, null=True, verbose_name="Autor")
    categoria = models.CharField(max_length=100, blank=True, null=True, verbose_name="Categoria Original")
    tags = ArrayField(models.CharField(max_length=50), blank=True, null=True, verbose_name="Tags")

    def __str__(self):
        return str(self.titulo)
    

    class Meta:
        verbose_name = "Notícia"
        verbose_name_plural = "Notícias"
        ordering = ['-data_publicacao'] # Ordena as notícias pela data de registro

class CategoriaModel(BaseModel):
    nome = models.CharField(max_length=255, verbose_name="Nome")
    

    def __str__(self):
        return str(self.nome)
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['nome']


class SubCategoriaModel(BaseModel):
    nome = models.CharField(max_length=255, verbose_name="Nome")
    categoria = models.ForeignKey(CategoriaModel, on_delete=models.CASCADE, verbose_name="Categoria")
    

    def __str__(self):
        return str(self.nome)
    
    class Meta:
        verbose_name = "SubCategoria"
        verbose_name_plural = "SubCategorias"
        ordering = ['nome']