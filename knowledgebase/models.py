from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from markdown import markdown
from django.utils.safestring import mark_safe
from ckeditor.fields import RichTextField  # optional; use TextField if no CKEditor

User = get_user_model()

class Category(models.Model):
    """
    Hierarchical categories for organizing articles.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="CSS class (e.g., 'fas fa-folder')")
    order = models.PositiveSmallIntegerField(default=0)
    is_public = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('knowledgebase:category', kwargs={'slug': self.slug})

    def get_ancestors(self):
        ancestors = []
        node = self
        while node.parent:
            ancestors.insert(0, node.parent)
            node = node.parent
        return ancestors


class Tag(models.Model):
    """
    Tags for articles (searchable).
    """
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Article(models.Model):
    """
    Knowledge base article.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='articles')
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles')

    # Content can be markdown or HTML
    content = models.TextField()
    content_html = models.TextField(blank=True, editable=False)

    # Excerpt for listings
    excerpt = models.CharField(max_length=300, blank=True)

    # Authoring
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Publishing
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)

    # Engagement
    views = models.PositiveIntegerField(default=0)
    helpful_count = models.PositiveIntegerField(default=0)
    not_helpful_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.content:
            # Convert markdown to HTML (if using markdown)
            self.content_html = markdown(self.content)
        if not self.excerpt and self.content:
            # Auto-generate excerpt from first 300 characters (strip markup)
            plain_text = self.content[:300]  # simple; can improve
            self.excerpt = plain_text[:300] + '...' if len(plain_text) > 300 else plain_text
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('knowledgebase:detail', kwargs={'slug': self.slug})

    def get_content_html(self):
        # If content is stored as markdown, render it
        return mark_safe(self.content_html)

    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def record_helpful(self, helpful=True):
        if helpful:
            self.helpful_count += 1
        else:
            self.not_helpful_count += 1
        self.save()


class ArticleFeedback(models.Model):
    """
    User feedback on article helpfulness.
    """
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='feedback')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    helpful = models.BooleanField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.article.title} - {'Helpful' if self.helpful else 'Not helpful'}"


class ArticleView(models.Model):
    """
    Detailed view logging for analytics.
    """
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_views')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.article.title} - {self.viewed_at.strftime('%Y-%m-%d')}"
