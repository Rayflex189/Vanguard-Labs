from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import FileExtensionValidator
import uuid

User = get_user_model()

class Conversation(models.Model):
    """
    A conversation between two or more users.
    """
    participants = models.ManyToManyField(User, through='Participant', related_name='conversations')
    subject = models.CharField(max_length=200, blank=True, null=True)
    is_group = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_message = models.ForeignKey('Message', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"Conversation #{self.id} - {self.subject or 'No Subject'}"

    def get_participant_for_user(self, user):
        try:
            return self.participant_set.get(user=user)
        except Participant.DoesNotExist:
            return None

    def get_unread_count_for_user(self, user):
        """Get number of unread messages for a specific user."""
        participant = self.get_participant_for_user(user)
        if not participant:
            return 0
        last_read = participant.last_read_at or timezone.datetime.min
        return self.message_set.filter(sent_at__gt=last_read).exclude(sender=user).count()

    def mark_as_read_for_user(self, user):
        """Mark all messages as read for a user."""
        participant = self.get_participant_for_user(user)
        if participant:
            participant.last_read_at = timezone.now()
            participant.save(update_fields=['last_read_at'])


class Participant(models.Model):
    """
    Intermediate model for tracking per-user conversation state.
    """
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)  # for group conversations
    is_muted = models.BooleanField(default=False)
    last_read_at = models.DateTimeField(blank=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('conversation', 'user')

    def __str__(self):
        return f"{self.user.username} in {self.conversation.id}"


class Message(models.Model):
    """
    Individual message within a conversation.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    attachment = models.FileField(
        upload_to='messaging/attachments/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'png', 'zip', 'txt'])]
    )
    sent_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['sent_at']

    def __str__(self):
        return f"Message from {self.sender.username} at {self.sent_at}"

    def mark_as_read_by(self, user):
        """Mark this message as read by a user."""
        receipt, created = MessageReadReceipt.objects.get_or_create(
            message=self,
            user=user,
            defaults={'read_at': timezone.now()}
        )
        if not created and not receipt.read_at:
            receipt.read_at = timezone.now()
            receipt.save(update_fields=['read_at'])
        return receipt

    def is_read_by(self, user):
        """Check if message has been read by user."""
        return MessageReadReceipt.objects.filter(message=self, user=user, read_at__isnull=False).exists()


class MessageReadReceipt(models.Model):
    """
    Tracks when a user reads a specific message.
    """
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('message', 'user')

    def __str__(self):
        return f"{self.user.username} read {self.message.id}"
