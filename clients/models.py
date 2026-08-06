# clients/models.py
from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='clients/logos/', blank=True)
    website = models.URLField(blank=True)
    industry = models.CharField(max_length=100, blank=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name
