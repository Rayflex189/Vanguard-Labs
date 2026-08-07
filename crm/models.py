from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from clients.models import Client
from team.models import TeamMember
from services.models import Service
from portfolio.models import Project
import uuid

User = get_user_model()

class Lead(models.Model):
    """
    A potential client/opportunity.
    """
    # Basic info
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    # Lead status
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('proposal', 'Proposal Sent'),
        ('negotiation', 'Negotiation'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    source = models.CharField(max_length=100, blank=True, help_text="Where did this lead come from?")
    score = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)], help_text="Lead score (0-100)")
    expected_value = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    probability = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)], help_text="Probability of closing (%)")

    # Relationships
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_leads')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_leads')
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, help_text="Converted client (when won)")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_contacted = models.DateTimeField(blank=True, null=True)

    # Additional
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['assigned_to']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.status}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def convert_to_client(self):
        """Convert lead to a Client and create associated ClientContact."""
        if self.status != 'won':
            return None
        client, created = Client.objects.get_or_create(
            name=self.company or f"{self.first_name} {self.last_name}",
            defaults={
                'primary_contact_name': self.get_full_name(),
                'primary_contact_email': self.email,
                'primary_contact_phone': self.phone,
                'status': 'active',
            }
        )
        self.client = client
        self.save()
        return client


class Opportunity(models.Model):
    """
    A specific opportunity tied to a lead or client.
    """
    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True, related_name='opportunities')
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name='opportunities')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    value = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    probability = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    expected_close_date = models.DateField(blank=True, null=True)

    STAGE_CHOICES = [
        ('prospecting', 'Prospecting'),
        ('discovery', 'Discovery'),
        ('proposal', 'Proposal'),
        ('negotiation', 'Negotiation'),
        ('closing', 'Closing'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    ]
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='prospecting')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.stage}"


class Interaction(models.Model):
    """
    Record of communication with a lead or client.
    """
    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True, related_name='interactions')
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name='interactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    TYPE_CHOICES = [
        ('call', 'Phone Call'),
        ('email', 'Email'),
        ('meeting', 'Meeting'),
        ('note', 'Note'),
        ('task', 'Task'),
        ('other', 'Other'),
    ]
    interaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='note')
    subject = models.CharField(max_length=200)
    details = models.TextField(blank=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.get_interaction_type_display()} - {self.subject}"


class Task(models.Model):
    """
    Tasks and to-dos for leads, clients, or opportunities.
    """
    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    opportunity = models.ForeignKey(Opportunity, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {'Completed' if self.completed else 'Pending'}"


class Note(models.Model):
    """
    Quick notes on leads/clients.
    """
    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True, related_name='notes')
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name='crm_notes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    is_internal = models.BooleanField(default=True, help_text="Visible only to staff")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Note by {self.user.username} - {self.created_at.strftime('%Y-%m-%d')}"
