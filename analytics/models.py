from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class PageView(models.Model):
    """
    Track every page request with detailed context.
    """
    # User and session
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)

    # Request details
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10, choices=[
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE'),
        ('PATCH', 'PATCH'),
    ], default='GET')
    query_string = models.TextField(blank=True, null=True)
    referer = models.URLField(max_length=500, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    accept_language = models.CharField(max_length=100, blank=True, null=True)

    # Response
    status_code = models.PositiveSmallIntegerField(default=200)
    response_time = models.FloatField(blank=True, null=True)  # in milliseconds

    # Timestamps
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['path', '-timestamp']),
            models.Index(fields=['user', '-timestamp']),
        ]
        ordering = ['-timestamp']
        verbose_name = "Page View"
        verbose_name_plural = "Page Views"

    def __str__(self):
        return f"{self.path} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class CustomEvent(models.Model):
    """
    Track custom events (e.g., button clicks, form submissions, downloads).
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)

    event_name = models.CharField(max_length=100)  # e.g., "signup_click", "project_download"
    event_category = models.CharField(max_length=100, blank=True, null=True)  # optional grouping
    event_label = models.CharField(max_length=255, blank=True, null=True)  # extra context
    event_value = models.IntegerField(blank=True, null=True)  # numeric value

    # Context
    page_path = models.CharField(max_length=255, blank=True, null=True)
    referer = models.URLField(max_length=500, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)

    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['event_name', '-timestamp']),
        ]
        ordering = ['-timestamp']
        verbose_name = "Custom Event"
        verbose_name_plural = "Custom Events"

    def __str__(self):
        return f"{self.event_name} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class DailyStats(models.Model):
    """
    Aggregated daily statistics for quick dashboard rendering.
    """
    date = models.DateField(unique=True)
    total_page_views = models.PositiveIntegerField(default=0)
    unique_visitors = models.PositiveIntegerField(default=0)  # based on distinct users/sessions
    total_events = models.PositiveIntegerField(default=0)
    average_response_time = models.FloatField(default=0.0)

    class Meta:
        ordering = ['-date']
        verbose_name = "Daily Stat"
        verbose_name_plural = "Daily Stats"

    def __str__(self):
        return self.date.isoformat()
