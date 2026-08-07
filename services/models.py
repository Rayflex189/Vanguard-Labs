from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

class ServiceCategory(models.Model):
    """
    Categories for grouping services (e.g., Development, Design, Consulting).
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="CSS class")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Service Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Service(models.Model):
    """
    Individual service offering.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='services')
    icon = models.CharField(max_length=50, help_text="CSS class (e.g., 'fas fa-code')")
    description = models.TextField()
    short_description = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='services/', blank=True, null=True)

    # Pricing (optional)
    pricing_model = models.CharField(max_length=20, choices=[
        ('fixed', 'Fixed Price'),
        ('hourly', 'Hourly'),
        ('monthly', 'Monthly Subscription'),
        ('custom', 'Custom Quote'),
    ], default='custom')
    base_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Base price if fixed")

    # Status
    is_active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)

    # Additional fields
    delivery_time = models.CharField(max_length=100, blank=True, help_text="e.g., 2 weeks")
    includes = models.TextField(blank=True, help_text="What's included (bullet list)")
    requirements = models.TextField(blank=True, help_text="Client requirements")
    faq = models.TextField(blank=True, help_text="Frequently asked questions")

    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('services:detail', kwargs={'slug': self.slug})


class ServiceFeature(models.Model):
    """
    Individual feature or benefit of a service (used on detail page).
    """
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='features')
    icon = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.service.name} - {self.title}"
