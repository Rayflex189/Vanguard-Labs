from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from portfolio.models import Project  # optional relationship
import uuid

User = get_user_model()

class Client(models.Model):
    """
    Main client model with company details and status tracking.
    """
    # Company info
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    logo = models.ImageField(upload_to='clients/logos/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    # Contact info (primary)
    primary_contact_name = models.CharField(max_length=100, blank=True, null=True)
    primary_contact_email = models.EmailField(blank=True, null=True)
    primary_contact_phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    # Status & classification
    STATUS_CHOICES = [
        ('lead', 'Lead'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('former', 'Former'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='lead')
    is_featured = models.BooleanField(default=False, help_text="Show on homepage/client showcase")

    # Internal
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_clients')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_clients')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Additional
    billing_cycle = models.CharField(max_length=50, blank=True, null=True)
    payment_terms = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['name']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('clients:detail', kwargs={'slug': self.slug})


class ClientContact(models.Model):
    """
    Multiple contacts per client.
    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='contacts')
    full_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return f"{self.full_name} - {self.client.name}"


class ClientProject(models.Model):
    """
    Projects associated with a client (could be from portfolio app).
    If you already have portfolio.Project, you can link via OneToOne or ForeignKey.
    Here we create a separate client-specific project model for flexibility.
    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[
        ('planning', 'Planning'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled'),
    ], default='planning')
    budget = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    technologies = models.CharField(max_length=200, blank=True, null=True, help_text="Comma separated")
    link_to_portfolio = models.ForeignKey('portfolio.Project', on_delete=models.SET_NULL, null=True, blank=True, help_text="Link to the main portfolio project")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.client.name} - {self.name}"


class ClientNote(models.Model):
    """
    Internal notes or communications log.
    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='notes')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    is_internal = models.BooleanField(default=True, help_text="Only visible to staff")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Note for {self.client.name} - {self.created_at.strftime('%Y-%m-%d')}"
