from django.db import models

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default='Vanguard Labs')
    tagline = models.CharField(max_length=200, default='Building Tomorrow\'s Digital Experiences.')
    logo = models.ImageField(upload_to='site/', blank=True)
    favicon = models.ImageField(upload_to='site/', blank=True)
    footer_text = models.TextField(blank=True)
    google_analytics_id = models.CharField(max_length=50, blank=True)
    meta_description = models.CharField(max_length=200, blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name_plural = 'Site Settings'

class CompanyStat(models.Model):
    label = models.CharField(max_length=50)   # e.g., "Projects Completed"
    value = models.IntegerField()
    icon = models.CharField(max_length=50, blank=True)  # CSS class
    order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.label}: {self.value}"

class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.question
