from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Page, Menu, MenuItem, SiteConfig

class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
    fields = ('label', 'parent', 'link_type', 'page', 'external_url', 'anchor', 'order', 'open_in_new_tab', 'is_active')
    ordering = ['order']

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [MenuItemInline]

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'is_published', 'publish_date', 'order', 'view_link')
    list_filter = ('is_published', 'parent', 'publish_date')
    search_fields = ('title', 'content', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['order']
    fieldsets = (
        ('Basic', {
            'fields': ('parent', 'title', 'slug', 'order')
        }),
        ('Content', {
            'fields': ('content', 'excerpt', 'template_name')
        }),
        ('SEO & Metadata', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords', 'og_image')
        }),
        ('Publishing', {
            'fields': ('is_published', 'publish_date', 'expiry_date', 'author')
        }),
    )

    def view_link(self, obj):
        if obj.is_published:
            url = obj.get_absolute_url()
            return format_html('<a href="{}" target="_blank">View</a>', url)
        return "-"
    view_link.short_description = "Preview"

@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Allow only one instance
        if SiteConfig.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    fieldsets = (
        ('Site Identity', {
            'fields': ('site_name', 'tagline', 'logo', 'favicon')
        }),
        ('Contact & Address', {
            'fields': ('contact_email', 'contact_phone', 'address')
        }),
        ('Footer', {
            'fields': ('footer_text', 'copyright_text')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords', 'google_analytics_id', 'google_tag_manager_id')
        }),
        ('Social Media', {
            'fields': ('social_facebook', 'social_twitter', 'social_instagram', 'social_linkedin', 'social_youtube', 'social_github')
        }),
    )
