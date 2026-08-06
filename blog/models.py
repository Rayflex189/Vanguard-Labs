from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from markdown import markdown
from django.utils.html import strip_tags
import re

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()  # Markdown
    excerpt = models.CharField(max_length=300, blank=True)
    cover_image = models.ImageField(upload_to='blog/')
    categories = models.ManyToManyField('blog.Category', blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey('team.TeamMember', on_delete=models.SET_NULL, null=True)
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.excerpt and self.content:
            # generate excerpt from first paragraph
            plain = strip_tags(markdown(self.content))
            self.excerpt = plain[:250] + '...' if len(plain) > 250 else plain
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    def reading_time(self):
        words = len(strip_tags(markdown(self.content)).split())
        return max(1, round(words / 200))  # avg 200 words/min

    def __str__(self):
        return self.title

class BlogCategory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
