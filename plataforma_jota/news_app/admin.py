from django.contrib import admin
from news_app.models import News, Category, Subcategory, Tag
# Register your models here.

admin.site.register(News)
admin.site.register(Category)
admin.site.register(Subcategory)