from django.contrib import admin
from django.utils.html import format_html
from .models import TestimonialCategory, Testimonial

@admin.register(TestimonialCategory)
class TestimonialCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = (
        'client_name', 'client_company', 'rating', 'is_published',
        'is_featured', 'created_at', 'thumbnail'
    )
    list_filter = ('is_published', 'is_featured', 'rating', 'categories')
    search_fields = ('client_name', 'client_company', 'content')
    fieldsets = (
        ('Client', {
            'fields': ('client_name', 'client_company', 'client_title', 'client_photo', 'client')
        }),
        ('Testimonial', {
            'fields': ('content', 'rating', 'video_url', 'project')
        }),
        ('Categories', {
            'fields': ('categories',)
        }),
        ('Status', {
            'fields': ('is_published', 'is_featured', 'featured_order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at', 'published_at')
    actions = ['publish_selected', 'unpublish_selected', 'feature_selected']

    def thumbnail(self, obj):
        if obj.client_photo:
            return format_html('<img src="{}" style="max-height:50px;"/>', obj.client_photo.url)
        return "-"
    thumbnail.short_description = 'Photo'

    def publish_selected(self, request, queryset):
        for obj in queryset:
            obj.publish()
        self.message_user(request, f"Published {queryset.count()} testimonials.")
    publish_selected.short_description = "Publish selected"

    def unpublish_selected(self, request, queryset):
        queryset.update(is_published=False, published_at=None)
        self.message_user(request, f"Unpublished {queryset.count()} testimonials.")
    unpublish_selected.short_description = "Unpublish selected"

    def feature_selected(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f"Featured {queryset.count()} testimonials.")
    feature_selected.short_description = "Feature selected"
