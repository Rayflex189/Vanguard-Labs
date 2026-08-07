from django.contrib import admin
from django.utils.html import format_html
from .models import TeamRole, TeamMember

@admin.register(TeamRole)
class TeamRoleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name',)

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'experience', 'is_active', 'is_featured', 'order')
    list_filter = ('role', 'is_active', 'is_featured')
    search_fields = ('name', 'bio', 'skills')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic', {
            'fields': ('name', 'slug', 'role', 'photo', 'bio', 'short_bio')
        }),
        ('Professional', {
            'fields': ('experience', 'skills', 'education', 'certifications')
        }),
        ('Contact & Social', {
            'fields': ('email', 'phone', 'github', 'linkedin', 'twitter', 'instagram', 'website')
        }),
        ('Display', {
            'fields': ('order', 'is_active', 'is_featured')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'joined_at'),
            'classes': ('collapse',)
        }),
    )

    def thumbnail(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height:50px;"/>', obj.photo.url)
        return "-"
    thumbnail.short_description = 'Photo'
