from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Task, ActivityLog

@receiver(post_save, sender=Task)
def log_task_save(sender, instance, created, **kwargs):
    action = 'Task created' if created else 'Task updated'
    ActivityLog.objects.create(
        project=instance.project,
        user=instance.created_by,
        action=action,
        details=f"Task '{instance.title}' - {action}"
    )

@receiver(post_delete, sender=Task)
def log_task_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(
        project=instance.project,
        user=instance.created_by,
        action='Task deleted',
        details=f"Task '{instance.title}' deleted"
    )
