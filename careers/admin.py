# careers/admin.py
from django.contrib import admin
from .models import JobOpening

@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'location', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
