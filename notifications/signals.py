from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Notification, NotificationCategory

User = get_user_model()

@receiver(post_save, sender=User)
def welcome_notification(sender, instance, created, **kwargs):
    if created:
        category, _ = NotificationCategory.objects.get_or_create(name='Welcome', slug='welcome')
        Notification.objects.create(
            recipient=instance,
            title='Welcome to Vanguard Labs!',
            message='We\'re excited to have you on board. Explore the platform and reach out if you need help.',
            category=category,
            link='/'
        )
