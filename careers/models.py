# careers/models.py
from django.db import models

class JobOpening(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    department = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField()
    is_active = models.BooleanField(default=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    closing_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
