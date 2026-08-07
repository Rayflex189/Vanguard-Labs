from django.contrib import admin
from django.utils.html import format_html
from .models import Conversation, Participant, Message, MessageReadReceipt

class ParticipantInline(admin.TabularInline):
    model = Participant
    extra = 1
    fields = ('user', 'is_admin', 'is_muted', 'last_read_at')
    readonly_fields = ('last_read_at',)

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    fields = ('sender', 'content_preview', 'sent_at', 'is_deleted')
    readonly_fields = ('sent_at',)
    ordering = ('-sent_at',)

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'is_group', 'created_at', 'updated_at', 'participant_count')
    list_filter = ('is_group', 'created_at')
    search_fields = ('subject', 'id')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ParticipantInline, MessageInline]

    def participant_count(self, obj):
        return obj.participants.count()
    participant_count.short_description = 'Participants'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'sender', 'content_preview', 'sent_at', 'is_deleted')
    list_filter = ('is_deleted', 'sent_at')
    search_fields = ('content', 'sender__username')
    readonly_fields = ('id', 'sent_at')
    fieldsets = (
        ('Message', {
            'fields': ('id', 'conversation', 'sender', 'content', 'attachment', 'sent_at', 'edited_at')
        }),
        ('Status', {
            'fields': ('is_deleted',)
        }),
    )

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'

@admin.register(MessageReadReceipt)
class MessageReadReceiptAdmin(admin.ModelAdmin):
    list_display = ('message', 'user', 'read_at')
    list_filter = ('read_at',)
