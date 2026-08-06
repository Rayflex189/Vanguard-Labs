from django.contrib import admin
from .models import PageView, CustomEvent, DailyStats

@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ('path', 'method', 'user', 'ip_address', 'status_code', 'timestamp')
    list_filter = ('method', 'status_code', 'timestamp')
    search_fields = ('path', 'user__username', 'ip_address')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'
    fieldsets = (
        ('Request', {
            'fields': ('path', 'method', 'query_string', 'status_code', 'response_time')
        }),
        ('Context', {
            'fields': ('user', 'session_key', 'referer', 'user_agent', 'ip_address', 'accept_language')
        }),
        ('Meta', {
            'fields': ('timestamp',)
        }),
    )

@admin.register(CustomEvent)
class CustomEventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'event_category', 'user', 'ip_address', 'timestamp')
    list_filter = ('event_name', 'event_category', 'timestamp')
    search_fields = ('event_name', 'event_label', 'user__username')
    readonly_fields = ('timestamp',)

@admin.register(DailyStats)
class DailyStatsAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_page_views', 'unique_visitors', 'total_events')
    readonly_fields = ('date',)
