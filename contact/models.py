from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator

class ContactCategory(models.Model):
    """
    Optional categories to classify incoming messages.
    """
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Contact Categories'
        ordering = ['name']

class ContactMessage(models.Model):
    """
    Stores contact form submissions.
    """
    # Personal info
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)

    # Message details
    subject = models.CharField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(ContactCategory, on_delete=models.SET_NULL, null=True, blank=True)
    service_interest = models.CharField(max_length=100, blank=True, null=True)
    project_budget = models.CharField(max_length=50, blank=True, null=True)
    timeline = models.CharField(max_length=50, blank=True, null=True)
    message = models.TextField()
    attachment = models.FileField(
        upload_to='contact_attachments/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'png', 'zip'])]
    )

    # Status and internal notes
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('spam', 'Spam'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    notes = models.TextField(blank=True, null=True, help_text="Internal staff notes")
    assigned_to = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)

    # IP and user‑agent for spam detection / analytics
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.name} - {self.email} ({self.created_at.strftime('%Y-%m-%d')})"
