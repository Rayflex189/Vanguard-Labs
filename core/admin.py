from django.contrib import admin
from .models import SiteSettings, CompanyStat, FAQ, NewsletterSubscriber

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if SiteSettings.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    fieldsets = (
        ('Identity', {
            'fields': ('site_name', 'tagline', 'logo', 'favicon', 'footer_text', 'copyright_text')
        }),
        ('Contact', {
            'fields': ('contact_email', 'contact_phone', 'address')
        }),
        ('Social Media', {
            'fields': ('social_facebook', 'social_twitter', 'social_instagram', 'social_linkedin', 'social_youtube', 'social_github')
        }),
        ('SEO & Analytics', {
            'fields': ('meta_description', 'meta_keywords', 'google_analytics_id', 'google_tag_manager_id')
        }),
        ('Maintenance', {
            'fields': ('enable_maintenance_mode', 'maintenance_message')
        }),
    )

@admin.register(CompanyStat)
class CompanyStatAdmin(admin.ModelAdmin):
    list_display = ('label', 'value', 'order')
    list_editable = ('value', 'order')
    ordering = ('order',)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'is_published')
    list_editable = ('order', 'is_published')
    search_fields = ('question', 'answer')

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('email',)
