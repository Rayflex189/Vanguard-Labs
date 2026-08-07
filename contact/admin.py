from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import ContactMessage, ContactCategory

@admin.register(ContactCategory)
class ContactCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'status', 'is_read', 'created_at')
    list_filter = ('status', 'is_read', 'category', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message', 'subject')
    readonly_fields = ('created_at', 'updated_at', 'ip_address', 'user_agent')
    actions = ['mark_as_read', 'mark_as_unread', 'mark_as_resolved', 'mark_as_spam']

    fieldsets = (
        ('Sender Information', {
            'fields': ('name', 'email', 'phone', 'company')
        }),
        ('Message Details', {
            'fields': ('subject', 'category', 'service_interest', 'project_budget', 'timeline', 'message')
        }),
        ('Attachment', {
            'fields': ('attachment', 'attachment_preview'),
            'classes': ('collapse',)
        }),
        ('Status & Internal', {
            'fields': ('status', 'assigned_to', 'notes', 'is_read')
        }),
        ('Technical', {
            'fields': ('ip_address', 'user_agent', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def attachment_preview(self, obj):
        if obj.attachment:
            return format_html('<a href="{}" target="_blank">Download</a>', obj.attachment.url)
        return "-"
    attachment_preview.short_description = 'Attachment'

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected as read"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected as unread"

    def mark_as_resolved(self, request, queryset):
        queryset.update(status='resolved')
    mark_as_resolved.short_description = "Mark selected as resolved"

    def mark_as_spam(self, request, queryset):
        queryset.update(status='spam')
    mark_as_spam.short_description = "Mark selected as spam"

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('attachment',)
        return self.readonly_fields
