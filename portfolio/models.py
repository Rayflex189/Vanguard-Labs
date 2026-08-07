from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from team.models import TeamMember
from testimonials.models import Testimonial
from clients.models import Client  # optional linkage

User = get_user_model()

class Category(models.Model):
    """
    Project categories (e.g., Web, Mobile, AI, Branding).
    """
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="CSS class")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Technology(models.Model):
    """
    Technologies used in projects.
    """
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="CSS class")
    color = models.CharField(max_length=20, blank=True, help_text="Hex color")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Project(models.Model):
    """
    Main project model with all case study fields.
    """
    # Basic Info
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(help_text="Short description for listing")
    client = models.CharField(max_length=100, blank=True, help_text="Client name")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    technologies = models.ManyToManyField(Technology, blank=True)

    # Dates & Duration
    completion_date = models.DateField()
    duration = models.CharField(max_length=50, blank=True, help_text="e.g., 3 months")

    # Media
    cover_image = models.ImageField(upload_to='portfolio/covers/')
    gallery_images = models.ManyToManyField('ProjectImage', blank=True)

    # Links
    live_demo_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)

    # Featured & Status
    featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)

    # Team & Testimonial
    team_members = models.ManyToManyField(TeamMember, blank=True)
    testimonial = models.OneToOneField(Testimonial, on_delete=models.SET_NULL, null=True, blank=True)

    # Case Study Sections (rich text / markdown)
    problem_statement = models.TextField(blank=True, help_text="What challenge did the client face?")
    solution = models.TextField(blank=True, help_text="How did we solve it?")
    process = models.TextField(blank=True, help_text="Our approach and workflow")
    results = models.TextField(blank=True, help_text="Outcome and metrics")
    lessons_learned = models.TextField(blank=True)

    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-completion_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('portfolio:detail', kwargs={'slug': self.slug})


class ProjectImage(models.Model):
    """
    Gallery image for a project.
    """
    image = models.ImageField(upload_to='portfolio/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images', null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.project.title if self.project else 'Unknown'}"
