# knowledgebase/admin.py
from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
