from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from portfolio.models import Project as PortfolioProject  # optional linkage
from clients.models import Client
from team.models import TeamMember

User = get_user_model()

class Project(models.Model):
    """
    Internal project management project (can link to portfolio.Project).
    """
    # Basic
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    # Relationships (optional)
    portfolio_project = models.OneToOneField(
        PortfolioProject,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Link to the portfolio project if this is the same"
    )
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)

    # Dates
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    estimated_hours = models.PositiveIntegerField(blank=True, null=True)

    # Status
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('active', 'Active'),
        ('on_hold', 'On Hold'),
        ('review', 'In Review'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ], default='medium')

    # Team
    project_manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_projects')
    team_members = models.ManyToManyField(TeamMember, blank=True, related_name='project_assignments')

    # Budget
    budget = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    actual_cost = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('projects_management:project_detail', kwargs={'slug': self.slug})

    def get_progress(self):
        """Calculate overall project progress based on tasks."""
        tasks = self.tasks.all()
        if not tasks:
            return 0
        completed = tasks.filter(status='completed').count()
        return int((completed / tasks.count()) * 100)


class Milestone(models.Model):
    """
    Major project milestones.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='milestones')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['due_date', 'order']

    def __str__(self):
        return f"{self.project.name} - {self.name}"


class Task(models.Model):
    """
    Individual tasks within a project.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    milestone = models.ForeignKey(Milestone, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subtasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_tasks')

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('review', 'In Review'),
        ('completed', 'Completed'),
        ('blocked', 'Blocked'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ], default='medium')

    due_date = models.DateField(blank=True, null=True)
    estimated_hours = models.PositiveIntegerField(blank=True, null=True)
    actual_hours = models.PositiveIntegerField(blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.project.name} - {self.title}"

    def get_absolute_url(self):
        return reverse('projects_management:task_detail', kwargs={'pk': self.pk})


class TimeLog(models.Model):
    """
    Time tracking for tasks.
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='time_logs')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    hours = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.task.title} - {self.hours}h"


class Comment(models.Model):
    """
    Comments on tasks or projects.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    attachment = models.FileField(upload_to='project_comments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.user.username} - {self.created_at}"


class ActivityLog(models.Model):
    """
    Log of project/task updates (similar to a feed).
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='activity_logs')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=200)
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.created_at}"
