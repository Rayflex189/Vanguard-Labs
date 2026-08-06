from django.contrib import admin
from .models import BlogPost, Tag, BlogCategory
from markdown import markdown
from django.utils.safestring import mark_safe

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'is_published', 'author')
    list_filter = ('is_published', 'categories', 'tags')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Main', {'fields': ('title', 'slug', 'content', 'cover_image', 'author')}),
        ('Metadata', {'fields': ('categories', 'tags', 'is_published')}),
    )

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
