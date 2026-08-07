from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Tag, Article, ArticleFeedback, ArticleView

class ArticleFeedbackInline(admin.TabularInline):
    model = ArticleFeedback
    extra = 0
    fields = ('helpful', 'comment', 'user', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'order', 'is_public')
    list_filter = ('is_public',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_published', 'is_featured', 'created_at', 'views')
    list_filter = ('is_published', 'is_featured', 'category', 'tags')
    search_fields = ('title', 'content', 'excerpt')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('views', 'helpful_count', 'not_helpful_count', 'created_at', 'updated_at')
    fieldsets = (
        ('Basic', {
            'fields': ('title', 'slug', 'category', 'tags')
        }),
        ('Content', {
            'fields': ('content', 'excerpt')
        }),
        ('Author & Publishing', {
            'fields': ('author', 'is_published', 'published_at', 'is_featured')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Analytics', {
            'fields': ('views', 'helpful_count', 'not_helpful_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    inlines = [ArticleFeedbackInline]

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing existing
            return self.readonly_fields + ('content_html',)
        return self.readonly_fields

@admin.register(ArticleFeedback)
class ArticleFeedbackAdmin(admin.ModelAdmin):
    list_display = ('article', 'helpful', 'user', 'created_at')
    list_filter = ('helpful', 'created_at')
    search_fields = ('article__title', 'comment')

@admin.register(ArticleView)
class ArticleViewAdmin(admin.ModelAdmin):
    list_display = ('article', 'user', 'viewed_at')
    list_filter = ('viewed_at',)
    readonly_fields = ('viewed_at',)
