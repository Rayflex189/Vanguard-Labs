from django.contrib import admin
from .models import ServiceCategory, Service, ServiceFeature

class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 1
    fields = ('icon', 'title', 'description', 'order')

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'order')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'pricing_model', 'base_price', 'featured', 'is_active')
    list_filter = ('category', 'is_active', 'featured', 'pricing_model')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic', {
            'fields': ('name', 'slug', 'category', 'icon', 'image')
        }),
        ('Content', {
            'fields': ('short_description', 'description')
        }),
        ('Pricing', {
            'fields': ('pricing_model', 'base_price')
        }),
        ('Details', {
            'fields': ('delivery_time', 'includes', 'requirements', 'faq')
        }),
        ('Status', {
            'fields': ('is_active', 'featured', 'order')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )
    inlines = [ServiceFeatureInline]
