from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Page(models.Model):
    """
    A CMS page with hierarchical structure.
    """
    # Hierarchical
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)  # will be generated if not provided

    # Content
    content = models.TextField(help_text="HTML content. Use <h1>, <p>, etc.")
    excerpt = models.CharField(max_length=300, blank=True)

    # Template and appearance
    TEMPLATE_CHOICES = [
        ('cms/page.html', 'Default'),
        ('cms/full_width.html', 'Full Width'),
        ('cms/landing.html', 'Landing Page'),
        # Add more as needed
    ]
    template_name = models.CharField(max_length=100, choices=TEMPLATE_CHOICES, default='cms/page.html')

    # Metadata
    meta_title = models.CharField(max_length=200, blank=True, help_text="If empty, uses page title")
    meta_description = models.CharField(max_length=300, blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)
    og_image = models.ImageField(upload_to='cms/og_images/', blank=True, null=True)

    # Publishing
    is_published = models.BooleanField(default=False)
    publish_date = models.DateTimeField(default=timezone.now)
    expiry_date = models.DateTimeField(blank=True, null=True)

    # Author and timestamps
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Order for navigation
    order = models.PositiveSmallIntegerField(default=0, help_text="Order in navigation lists")

    class Meta:
        ordering = ['order', 'title']
        unique_together = ('parent', 'slug')  # slugs unique per parent

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # Build full path from ancestors
        if self.parent:
            return reverse('cms:page', kwargs={'path': self.get_full_path()})
        else:
            return reverse('cms:page', kwargs={'path': self.slug})

    def get_full_path(self):
        """Return full slug path (e.g., 'about/team')"""
        if self.parent:
            return f"{self.parent.get_full_path()}/{self.slug}"
        return self.slug

    def get_ancestors(self):
        """Return list of ancestors (including self) from root to current"""
        ancestors = []
        node = self
        while node:
            ancestors.insert(0, node)
            node = node.parent
        return ancestors

    def get_children(self):
        return self.children.filter(is_published=True)


class Menu(models.Model):
    """
    A navigation menu (e.g., Main Menu, Footer Menu).
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """
    Individual item within a menu.
    """
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    label = models.CharField(max_length=100)
    link_type = models.CharField(max_length=20, choices=[
        ('page', 'Page'),
        ('external', 'External URL'),
        ('anchor', 'Anchor Link'),
    ], default='page')
    page = models.ForeignKey(Page, on_delete=models.SET_NULL, null=True, blank=True, help_text="If link_type is 'page'")
    external_url = models.URLField(blank=True, null=True, help_text="If link_type is 'external'")
    anchor = models.CharField(max_length=100, blank=True, null=True, help_text="If link_type is 'anchor' e.g., #section")
    order = models.PositiveSmallIntegerField(default=0)
    open_in_new_tab = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.menu.name} - {self.label}"

    def get_url(self):
        if self.link_type == 'page' and self.page:
            return self.page.get_absolute_url()
        elif self.link_type == 'external':
            return self.external_url
        elif self.link_type == 'anchor':
            return self.anchor
        return '#'


class SiteConfig(models.Model):
    """
    Singleton site-wide settings.
    """
    site_name = models.CharField(max_length=100, default='Vanguard Labs')
    tagline = models.CharField(max_length=200, default='Building Tomorrow\'s Digital Experiences.')
    logo = models.ImageField(upload_to='cms/site/', blank=True, null=True)
    favicon = models.ImageField(upload_to='cms/site/', blank=True, null=True)
    footer_text = models.TextField(blank=True)
    copyright_text = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)
    google_analytics_id = models.CharField(max_length=50, blank=True)
    google_tag_manager_id = models.CharField(max_length=50, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    social_facebook = models.URLField(blank=True)
    social_twitter = models.URLField(blank=True)
    social_instagram = models.URLField(blank=True)
    social_linkedin = models.URLField(blank=True)
    social_youtube = models.URLField(blank=True)
    social_github = models.URLField(blank=True)

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = 'Site Configuration'
        verbose_name_plural = 'Site Configuration'

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SiteConfig.objects.exists():
            raise ValueError("There is already a SiteConfig instance.")
        super().save(*args, **kwargs)
