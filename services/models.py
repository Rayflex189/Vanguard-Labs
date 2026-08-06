from django.db import models
from django.utils.text import slugify

class Service(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50)  # Font Awesome or Heroicon class
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
