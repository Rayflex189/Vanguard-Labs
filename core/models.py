from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class SiteSettings(models.Model):
    """
    Singleton site-wide configuration.
    """
    # Identity
    site_name = models.CharField(max_length=100, default='Vanguard Labs')
    tagline = models.CharField(max_length=200, default='Building Tomorrow\'s Digital Experiences.')
    logo = models.ImageField(upload_to='core/site/', blank=True, null=True)
    favicon = models.ImageField(upload_to='core/site/', blank=True, null=True)
    footer_text = models.TextField(blank=True, help_text="Text displayed in footer.")
    copyright_text = models.CharField(max_length=200, blank=True, default='© Vanguard Labs. All rights reserved.')

    # Contact
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    # Social
    social_facebook = models.URLField(blank=True)
    social_twitter = models.URLField(blank=True)
    social_instagram = models.URLField(blank=True)
    social_linkedin = models.URLField(blank=True)
    social_youtube = models.URLField(blank=True)
    social_github = models.URLField(blank=True)

    # SEO
    meta_description = models.CharField(max_length=300, blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)
    google_analytics_id = models.CharField(max_length=50, blank=True)
    google_tag_manager_id = models.CharField(max_length=50, blank=True)

    # Other
    enable_maintenance_mode = models.BooleanField(default=False)
    maintenance_message = models.TextField(blank=True)

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def save(self, *args, **kwargs):
        if not self.pk and SiteSettings.objects.exists():
            raise ValueError("There is already a SiteSettings instance.")
        super().save(*args, **kwargs)


class CompanyStat(models.Model):
    """
    Statistics displayed on the homepage (e.g., "Projects Completed").
    """
    label = models.CharField(max_length=100)
    value = models.PositiveIntegerField()
    icon = models.CharField(max_length=50, blank=True, help_text="CSS class for icon (e.g., 'fas fa-code')")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Company Stat'
        verbose_name_plural = 'Company Stats'

    def __str__(self):
        return f"{self.label}: {self.value}"


class FAQ(models.Model):
    """
    Frequently Asked Questions (displayed on /faq or contact page).
    """
    question = models.CharField(max_length=200)
    answer = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question


class NewsletterSubscriber(models.Model):
    """
    Email subscribers for newsletter.
    """
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email
