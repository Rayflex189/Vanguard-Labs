from django.contrib import admin
from django.utils.html import format_html
from .models import Client, ClientContact, ClientProject, ClientNote

class ClientContactInline(admin.TabularInline):
    model = ClientContact
    extra = 1
    fields = ('full_name', 'job_title', 'email', 'phone', 'is_primary')

class ClientProjectInline(admin.TabularInline):
    model = ClientProject
    extra = 1
    fields = ('name', 'status', 'start_date', 'end_date', 'budget')
    show_change_link = True

class ClientNoteInline(admin.TabularInline):
    model = ClientNote
    extra = 1
    fields = ('content', 'author', 'is_internal')
    readonly_fields = ('author',)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'status', 'is_featured', 'assigned_to', 'primary_contact')
    list_filter = ('status', 'is_featured', 'industry', 'created_at')
    search_fields = ('name', 'website', 'primary_contact_email', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)
    fieldsets = (
        ('Company Info', {
            'fields': ('name', 'slug', 'logo', 'website', 'industry', 'description')
        }),
        ('Primary Contact', {
            'fields': ('primary_contact_name', 'primary_contact_email', 'primary_contact_phone')
        }),
        ('Address', {
            'fields': ('address', 'city', 'country')
        }),
        ('Status & Classification', {
            'fields': ('status', 'is_featured')
        }),
        ('Internal', {
            'fields': ('assigned_to', 'created_by', 'billing_cycle', 'payment_terms', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ClientContactInline, ClientProjectInline, ClientNoteInline]

    def primary_contact(self, obj):
        if obj.primary_contact_name:
            return f"{obj.primary_contact_name} ({obj.primary_contact_email})"
        return "-"
    primary_contact.short_description = "Primary Contact"

@admin.register(ClientContact)
class ClientContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'client', 'job_title', 'email', 'phone', 'is_primary')
    list_filter = ('client', 'is_primary')
    search_fields = ('full_name', 'email', 'phone')

@admin.register(ClientProject)
class ClientProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'status', 'start_date', 'end_date')
    list_filter = ('status', 'client')
    search_fields = ('name', 'description')

@admin.register(ClientNote)
class ClientNoteAdmin(admin.ModelAdmin):
    list_display = ('client', 'author', 'is_internal', 'created_at')
    list_filter = ('is_internal', 'created_at')
    search_fields = ('content',)
