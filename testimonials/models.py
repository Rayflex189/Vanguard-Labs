from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from clients.models import Client  # optional relationship
from portfolio.models import Project  # optional relationship

class TestimonialCategory(models.Model):
    """
    Optional categories for testimonials (e.g., Web, Mobile, Branding).
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Testimonial Categories"

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    """
    Client testimonial with rating and multimedia.
    """
    # Client info
    client_name = models.CharField(max_length=100)
    client_company = models.CharField(max_length=100, blank=True)
    client_photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    client_title = models.CharField(max_length=100, blank=True, help_text="Job title")

    # Optional relationship to Client model
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)

    # Content
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating out of 5"
    )

    # Categories
    categories = models.ManyToManyField(TestimonialCategory, blank=True)

    # Media
    video_url = models.URLField(blank=True, help_text="YouTube/Vimeo embed URL")
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, help_text="Related project")

    # Status & moderation
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    featured_order = models.PositiveSmallIntegerField(default=0, help_text="Order on featured carousel")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.client_name} - {self.rating}/5"

    def publish(self):
        if not self.is_published:
            self.is_published = True
            self.published_at = timezone.now()
            self.save(update_fields=['is_published', 'published_at'])
