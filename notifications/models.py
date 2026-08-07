from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import uuid

User = get_user_model()

class NotificationCategory(models.Model):
    """
    Categories for notifications (e.g., System, Message, Project, Event).
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True, help_text="CSS class (e.g., 'fas fa-info')")
    description = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Notification(models.Model):
    """
    Individual notification for a user.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_notifications')
    category = models.ForeignKey(NotificationCategory, on_delete=models.SET_NULL, null=True, blank=True)

    # Content
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.URLField(blank=True, null=True, help_text="URL to navigate when notification is clicked")
    link_text = models.CharField(max_length=100, blank=True, help_text="Text for the link button")

    # Read status
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(blank=True, null=True)

    # Delivery
    DELIVERY_CHANNELS = [
        ('in_app', 'In App'),
        ('email', 'Email'),
        ('push', 'Push Notification'),
        ('sms', 'SMS'),
    ]
    channel = models.CharField(max_length=20, choices=DELIVERY_CHANNELS, default='in_app')
    is_delivered = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(blank=True, null=True)

    # Action status (if user needs to act)
    ACTION_CHOICES = [
        ('none', 'None'),
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    action_status = models.CharField(max_length=20, choices=ACTION_CHOICES, default='none')
    action_response = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.title} for {self.recipient.username}"

    def get_absolute_url(self):
        if self.link:
            return self.link
        return reverse('notifications:detail', kwargs={'pk': self.pk})

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])
        return self

    def mark_as_unread(self):
        self.is_read = False
        self.read_at = None
        self.save(update_fields=['is_read', 'read_at'])
        return self

    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False

    def send_email(self):
        """Send notification as email."""
        if self.channel not in ['email', 'push']:
            return
        subject = f"[{settings.SITE_NAME}] {self.title}"
        context = {
            'notification': self,
            'site_name': settings.SITE_NAME or 'Vanguard Labs',
            'protocol': 'https' if not settings.DEBUG else 'http',
            'domain': settings.SITE_DOMAIN or 'localhost:8000',
        }
        html_body = render_to_string('notifications/email_notification.html', context)
        plain_body = render_to_string('notifications/email_notification.txt', context)
        send_mail(
            subject=subject,
            message=plain_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.recipient.email],
            html_message=html_body,
            fail_silently=True,
        )
        self.is_delivered = True
        self.delivered_at = timezone.now()
        self.save(update_fields=['is_delivered', 'delivered_at'])


class NotificationPreference(models.Model):
    """
    User preferences for email/push notifications per category.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_preferences')
    category = models.ForeignKey(NotificationCategory, on_delete=models.CASCADE)
    email_enabled = models.BooleanField(default=True)
    push_enabled = models.BooleanField(default=True)
    in_app_enabled = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'category')

    def __str__(self):
        return f"{self.user.username} - {self.category.name}"
