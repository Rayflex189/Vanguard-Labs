from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class TeamRole(models.Model):
    """
    Predefined roles (e.g., CEO, Developer, Designer) for categorization.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    """
    Individual team member profile.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    role = models.ForeignKey(TeamRole, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    bio = models.TextField()
    short_bio = models.CharField(max_length=200, blank=True)

    # Professional details
    experience = models.PositiveIntegerField(help_text="Years of experience")
    skills = models.CharField(max_length=200, help_text="Comma-separated list of skills")
    education = models.TextField(blank=True, help_text="Education background")
    certifications = models.TextField(blank=True)

    # Social links
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)

    # Order for display
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)

    # Timestamps
    joined_at = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('team:detail', kwargs={'slug': self.slug})

    def get_skills_list(self):
        """Return skills as a list."""
        return [s.strip() for s in self.skills.split(',') if s.strip()]
