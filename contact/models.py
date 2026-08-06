from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    company = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    project_budget = models.CharField(max_length=50, blank=True)
    service_interest = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    timeline = models.CharField(max_length=50, blank=True)
    attachment = models.FileField(upload_to='contact_attachments/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name} - {self.created_at}"
