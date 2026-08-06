from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

class Technology(models.Model):
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=50, help_text='CSS class for icon')

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    client = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    technologies = models.ManyToManyField(Technology)
    completion_date = models.DateField()
    cover_image = models.ImageField(upload_to='projects/covers/')
    gallery_images = models.ManyToManyField('ProjectImage', blank=True)
    live_demo_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    featured = models.BooleanField(default=False)
    duration = models.CharField(max_length=50, blank=True)
    team_members = models.ManyToManyField('team.TeamMember', blank=True)
    testimonial = models.OneToOneField('testimonials.Testimonial', on_delete=models.SET_NULL, null=True, blank=True)
    results = models.TextField(blank=True)
    problem_statement = models.TextField(blank=True)
    solution = models.TextField(blank=True)
    process = models.TextField(blank=True)
    lessons_learned = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('portfolio:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

class ProjectImage(models.Model):
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images', null=True)

    def __str__(self):
        return f"Image for {self.project.title if self.project else 'unknown'}"
