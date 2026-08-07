from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EventRegistration
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=EventRegistration)
def registration_created(sender, instance, created, **kwargs):
    if created:
        # Could trigger welcome email, add to mailchimp, etc.
        logger.info(f"New registration for {instance.event.title} by {instance.email}")
