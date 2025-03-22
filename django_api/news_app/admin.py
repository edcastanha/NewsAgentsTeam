from django.contrib import admin
from .models import NewsModel, CategoriaModel, SubCategoriaModel

admin.site.register(NewsModel)
admin.site.register(CategoriaModel)
admin.site.register(SubCategoriaModel)