from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import (
    EventCategory, Venue, Event, EventImage,
    EventRegistration, EventReminder
)

class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1

class EventRegistrationInline(admin.TabularInline):
    model = EventRegistration
    extra = 0
    fields = ('full_name', 'email', 'status', 'payment_status', 'checked_in')
    readonly_fields = ('created_at',)

@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name',)

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country', 'capacity', 'is_virtual')
    search_fields = ('name', 'address', 'city')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'category', 'status', 'is_free', 'is_featured')
    list_filter = ('status', 'category', 'is_free', 'is_featured', 'start_date')
    search_fields = ('title', 'description', 'short_description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'attendee_count', 'available_spots')
    fieldsets = (
        ('Basic', {
            'fields': ('title', 'slug', 'short_description', 'description', 'category')
        }),
        ('Venue & Time', {
            'fields': ('venue', 'start_date', 'end_date', 'registration_deadline')
        }),
        ('Capacity & Pricing', {
            'fields': ('max_attendees', 'price', 'is_free')
        }),
        ('Media', {
            'fields': ('cover_image', 'gallery_images')
        }),
        ('Organizer & Speakers', {
            'fields': ('organizer', 'speakers')
        }),
        ('Status & SEO', {
            'fields': ('status', 'is_featured', 'meta_title', 'meta_description')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    inlines = [EventImageInline, EventRegistrationInline]

    def attendee_count(self, obj):
        return obj.registrations.filter(status__in=['confirmed', 'attended']).count()
    attendee_count.short_description = "Confirmed Attendees"

    def available_spots(self, obj):
        if obj.max_attendees:
            taken = obj.registrations.filter(status__in=['confirmed', 'attended', 'pending']).count()
            return obj.max_attendees - taken
        return "Unlimited"
    available_spots.short_description = "Available Spots"

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'event', 'status', 'payment_status', 'checked_in', 'created_at')
    list_filter = ('status', 'payment_status', 'event', 'checked_in')
    search_fields = ('full_name', 'email', 'company')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['mark_as_confirmed', 'mark_as_attended', 'send_reminder']

    def mark_as_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
    mark_as_confirmed.short_description = "Mark selected as confirmed"

    def mark_as_attended(self, request, queryset):
        queryset.update(status='attended', checked_in=True, checked_in_at=timezone.now())
    mark_as_attended.short_description = "Mark selected as attended"

    def send_reminder(self, request, queryset):
        # Placeholder for bulk reminder sending
        self.message_user(request, "Reminder sending not implemented yet.")
    send_reminder.short_description = "Send reminder to selected"

@admin.register(EventReminder)
class EventReminderAdmin(admin.ModelAdmin):
    list_display = ('event', 'subject', 'send_time', 'sent')
    list_filter = ('sent',)
