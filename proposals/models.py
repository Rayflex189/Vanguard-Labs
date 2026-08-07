from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from clients.models import Client
from portfolio.models import Project as PortfolioProject
from services.models import Service
from team.models import TeamMember

User = get_user_model()

class ProposalStatus(models.Model):
    """
    Customizable statuses (e.g., Draft, Sent, Accepted, Rejected, etc.)
    """
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    color = models.CharField(max_length=20, default='#6B7280', help_text="Hex color")
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class ProposalTemplate(models.Model):
    """
    Pre-defined templates for proposals (content sections).
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    content = models.TextField(help_text="Template content (Markdown/HTML)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Proposal(models.Model):
    """
    Main proposal document.
    """
    # Identifiers
    proposal_number = models.CharField(max_length=50, unique=True, blank=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    # Relationships
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name='proposals')
    project = models.ForeignKey(PortfolioProject, on_delete=models.SET_NULL, null=True, blank=True)
    services = models.ManyToManyField(Service, blank=True, related_name='proposals')
    status = models.ForeignKey(ProposalStatus, on_delete=models.SET_NULL, null=True, blank=True)

    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sent_at = models.DateTimeField(blank=True, null=True)
    valid_until = models.DateField(blank=True, null=True)

    # Content
    content = models.TextField(help_text="Main content of the proposal (Markdown/HTML)")
    executive_summary = models.TextField(blank=True)

    # Financial
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Tax %")
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Meta
    currency = models.CharField(max_length=10, default='USD')
    notes = models.TextField(blank=True, help_text="Internal notes for staff")
    terms = models.TextField(blank=True, help_text="Terms and conditions")

    # Tracking
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_proposals')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_proposals')
    team_members = models.ManyToManyField(TeamMember, blank=True)

    # Optional template
    template = models.ForeignKey(ProposalTemplate, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        if not self.proposal_number:
            # Simple number generator: PROPOSAL-YYYYMMDD-XXXX
            from datetime import datetime
            prefix = datetime.now().strftime('PROPOSAL-%Y%m%d')
            last = Proposal.objects.filter(proposal_number__startswith=prefix).count()
            self.proposal_number = f"{prefix}-{str(last+1).zfill(4)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.proposal_number} - {self.title}"

    def get_absolute_url(self):
        return reverse('proposals:detail', kwargs={'slug': self.slug})


class ProposalLineItem(models.Model):
    """
    Line items within a proposal (services/products with quantity and price).
    """
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name='line_items')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.proposal.proposal_number} - {self.description}"


class ProposalComment(models.Model):
    """
    Internal or client-facing comments.
    """
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    is_internal = models.BooleanField(default=True, help_text="Visible only to staff")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.proposal.proposal_number} by {self.user.username}"
