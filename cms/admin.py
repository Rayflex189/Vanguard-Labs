# cms/admin.py
from django.contrib import admin
from .models import Page

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
