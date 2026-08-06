from django.contrib import admin
from .models import Project, Category, Technology, ProjectImage
from django.utils.html import format_html

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'category', 'featured', 'completion_date')
    list_filter = ('category', 'featured', 'technologies')
    search_fields = ('title', 'client', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]
    fieldsets = (
        ('Basic Info', {'fields': ('title', 'slug', 'description', 'client', 'category', 'technologies')}),
        ('Media', {'fields': ('cover_image', 'gallery_images')}),
        ('Details', {'fields': ('completion_date', 'duration', 'featured')}),
        ('Links', {'fields': ('live_demo_url', 'github_url')}),
        ('Case Study Content', {
            'classes': ('collapse',),
            'fields': ('problem_statement', 'solution', 'process', 'results', 'lessons_learned', 'testimonial')
        }),
        ('Team', {'fields': ('team_members',)}),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name',)

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name',)
