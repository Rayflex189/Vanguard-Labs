from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Technology, Project, ProjectImage

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ('image', 'caption', 'order')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'order')

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'category', 'completion_date', 'featured', 'is_published')
    list_filter = ('category', 'featured', 'is_published', 'completion_date', 'technologies')
    search_fields = ('title', 'client', 'description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic', {
            'fields': ('title', 'slug', 'description', 'client', 'category', 'technologies')
        }),
        ('Dates & Duration', {
            'fields': ('completion_date', 'duration')
        }),
        ('Media', {
            'fields': ('cover_image', 'gallery_images')
        }),
        ('Links', {
            'fields': ('live_demo_url', 'github_url')
        }),
        ('Status', {
            'fields': ('featured', 'is_published')
        }),
        ('Team & Testimonial', {
            'fields': ('team_members', 'testimonial')
        }),
        ('Case Study', {
            'fields': ('problem_statement', 'solution', 'process', 'results', 'lessons_learned'),
            'classes': ('collapse',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    inlines = [ProjectImageInline]
