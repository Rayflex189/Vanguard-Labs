from django.contrib import admin
from django.utils.html import format_html
from .models import NotificationCategory, Notification, NotificationPreference

@admin.register(NotificationCategory)
class NotificationCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'is_active')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'recipient', 'sender', 'category', 'is_read', 'channel', 'created_at', 'action_status')
    list_filter = ('is_read', 'channel', 'category', 'created_at', 'action_status')
    search_fields = ('title', 'message', 'recipient__username', 'sender__username')
    readonly_fields = ('id', 'created_at', 'read_at', 'delivered_at')
    fieldsets = (
        ('Recipients', {
            'fields': ('recipient', 'sender', 'category')
        }),
        ('Content', {
            'fields': ('title', 'message', 'link', 'link_text')
        }),
        ('Delivery', {
            'fields': ('channel', 'is_delivered', 'delivered_at')
        }),
        ('Read Status', {
            'fields': ('is_read', 'read_at')
        }),
        ('Action', {
            'fields': ('action_status', 'action_response')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'expires_at'),
            'classes': ('collapse',)
        }),
    )
    actions = ['mark_as_read', 'mark_as_unread', 'send_email']

    def mark_as_read(self, request, queryset):
        for obj in queryset:
            obj.mark_as_read()
    mark_as_read.short_description = "Mark selected as read"

    def mark_as_unread(self, request, queryset):
        for obj in queryset:
            obj.mark_as_unread()
    mark_as_unread.short_description = "Mark selected as unread"

    def send_email(self, request, queryset):
        sent = 0
        for obj in queryset:
            if obj.recipient.email:
                obj.send_email()
                sent += 1
        self.message_user(request, f"Email sent for {sent} notifications.")
    send_email.short_description = "Send email for selected"

@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'email_enabled', 'push_enabled', 'in_app_enabled')
    list_filter = ('email_enabled', 'push_enabled', 'in_app_enabled')
