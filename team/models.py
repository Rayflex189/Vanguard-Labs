from django.db import models
from django.urls import reverse

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='team/')
    role = models.CharField(max_length=100)
    bio = models.TextField()
    skills = models.CharField(max_length=200, help_text='Comma separated')
    experience = models.IntegerField(help_text='Years of experience')
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    social_media = models.JSONField(default=dict, blank=True)  # e.g. {"twitter": "url"}
    order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name
