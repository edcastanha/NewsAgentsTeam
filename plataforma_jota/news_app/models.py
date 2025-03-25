from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django_prometheus.models import ExportModelOperationsMixin


class BaseModel(models.Model):
    """
    Modelo base com campos de data de criação e atualização.
    """
    created_at = models.DateTimeField(_('Criado em'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Atualizado em'), auto_now=True)

    class Meta:
        abstract = True

class Category(ExportModelOperationsMixin('category'), BaseModel):
    """
    Representa uma categoria principal de notícias (vertical).
    Exemplos: Poder, Tributos, Saúde, Trabalhista.
    """
    name = models.CharField(_('Nome'), max_length=100, unique=True)
    description = models.TextField(_('Descrição'), blank=True)
    slug = models.SlugField(_('Slug'), max_length=100, unique=True)
    
    class Meta:
        verbose_name = _('Categoria')
        verbose_name_plural = _('Categorias')
        ordering = ['name']

    def __str__(self):
        return self.name

class Subcategory(ExportModelOperationsMixin('subcategory'), BaseModel):
    """
    Representa uma subcategoria de notícias.
    Exemplos: Aposta da Semana (dentro de Tributos), Matinal.
    """
    name = models.CharField(_('Nome'), max_length=100)
    description = models.TextField(_('Descrição'), blank=True)
    slug = models.SlugField(_('Slug'), max_length=100)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name=_('Categoria')
    )
    class Meta:
        verbose_name = _('Subcategoria')
        verbose_name_plural = _('Subcategorias')
        ordering = ['category__name', 'name']
        unique_together = ['slug', 'category']

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class Tag(ExportModelOperationsMixin('tag'), BaseModel):
    """
    Representa uma tag ou palavra-chave usada para classificar notícias.
    Exemplos: Reforma Tributária, Imposto de Renda, Saúde Pública.
    """
    name = models.CharField(_('Nome'), max_length=100, unique=True)
    slug = models.SlugField(_('Slug'), max_length=100, unique=True)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ['name']

    def __str__(self):
        return self.name

class Source(ExportModelOperationsMixin('source'), BaseModel):
    """
    Representa uma fonte de notícias original e os dados pré-processados (Normalizado).
    """
    raw_data = models.JSONField(_('Dados brutos'), null=False, blank=False)
    clean_data = models.JSONField(_('Dados limpos'), null=True, blank=True)
    processed_data = models.JSONField(_('Data de Processamento'), null=True, blank=True)
    is_processed = models.BooleanField(_('Processado'), default=False)
    name_source = models.CharField(_('Nome da Fonte'), max_length=255,  null=False, blank=False)
    
    class Meta:
        verbose_name = _('Fonte')
        verbose_name_plural = _('Fontes')
        ordering = ['processed_data']

    def __str__(self):
        return self.name

class News(ExportModelOperationsMixin('news'), BaseModel):
    """
    Representa uma notícia no sistema.
    """
    title = models.CharField(_('Título'), max_length=255)
    content = models.TextField(_('Conteúdo'))
    published_at = models.DateTimeField(_('Publicado em'), default=timezone.now)
    # Classificação
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='news',
        verbose_name=_('Categoria'),
        null=True,
        blank=True
    )
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.PROTECT,
        related_name='news',
        verbose_name=_('Subcategoria'),
        null=True,
        blank=True
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='news',
        verbose_name=_('Tags'),
        blank=True
    )
    # Flags
    is_urgent = models.BooleanField(_('Urgente'), default=False)
    is_classified = models.BooleanField(_('Classificado'), default=False)
    source = models.ForeignKey(
        Source,
        on_delete=models.PROTECT,
        related_name='news',
        verbose_name=_('Fonte'),
        null=False,
        blank=False
    )


    class Meta:
        verbose_name = _('Notícia')
        verbose_name_plural = _('Notícias')
        ordering = ['-is_urgent','-published_at']
        indexes = [
            models.Index(fields=['published_at']),
            models.Index(fields=['is_urgent']),
            models.Index(fields=['is_classified']),
        ]

    def __str__(self):
        return self.title
    
