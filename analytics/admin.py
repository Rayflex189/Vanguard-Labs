# analytics/admin.py
from django.contrib import admin
from .models import PageVisit

@admin.register(PageVisit)
class PageVisitAdmin(admin.ModelAdmin):
    list_display = ('path', 'timestamp', 'user')
    list_filter = ('timestamp',)
