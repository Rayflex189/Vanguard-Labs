from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from team.models import TeamMember

User = get_user_model()

class EventCategory(models.Model):
    """
    Categories for events (e.g., Workshop, Conference, Webinar).
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="CSS class for icon")

    class Meta:
        verbose_name_plural = "Event Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Venue(models.Model):
    """
    Physical or virtual venue for events.
    """
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    capacity = models.PositiveIntegerField(blank=True, null=True)
    is_virtual = models.BooleanField(default=False, help_text="Check if this is an online venue")
    meeting_link = models.URLField(blank=True, help_text="Zoom/Google Meet link if virtual")
    map_embed_url = models.URLField(blank=True, help_text="Google Maps embed URL")
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    """
    Main event model with all details.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    category = models.ForeignKey(EventCategory, on_delete=models.SET_NULL, null=True, blank=True)
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True, blank=True)

    # Date/time
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    registration_deadline = models.DateTimeField(blank=True, null=True)

    # Capacity & pricing
    max_attendees = models.PositiveIntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_free = models.BooleanField(default=False)

    # Image & media
    cover_image = models.ImageField(upload_to='events/covers/', blank=True, null=True)
    gallery_images = models.ManyToManyField('EventImage', blank=True)

    # Organizer & speakers
    organizer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='organized_events')
    speakers = models.ManyToManyField(TeamMember, blank=True, related_name='speaking_events')

    # Status
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('cancelled', 'Cancelled'),
        ('postponed', 'Postponed'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)

    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['start_date']),
            models.Index(fields=['status']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.start_date.strftime('%Y-%m-%d')})"

    def get_absolute_url(self):
        return reverse('events:detail', kwargs={'slug': self.slug})

    @property
    def is_upcoming(self):
        return self.start_date > timezone.now()

    @property
    def is_past(self):
        return self.end_date < timezone.now()

    @property
    def is_ongoing(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    @property
    def registration_open(self):
        if self.registration_deadline:
            return timezone.now() <= self.registration_deadline
        return self.is_upcoming


class EventImage(models.Model):
    """
    Gallery images for events.
    """
    image = models.ImageField(upload_to='events/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images', null=True)

    def __str__(self):
        return f"Image for {self.event.title if self.event else 'unknown'}"[:50]


class EventRegistration(models.Model):
    """
    Attendee registration for an event.
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='event_registrations')
    email = models.EmailField(help_text="Email for non-registered users")
    full_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    # Status & payment
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('waitlist', 'Waitlist'),
        ('attended', 'Attended'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=[
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    ], default='unpaid')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Additional
    special_requests = models.TextField(blank=True)
    checked_in = models.BooleanField(default=False)
    checked_in_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('event', 'email')  # prevent duplicate registration per email

    def __str__(self):
        return f"{self.full_name} - {self.event.title}"


class EventReminder(models.Model):
    """
    Scheduled reminders for event registrants.
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reminders')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    send_time = models.DateTimeField()
    sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Reminder for {self.event.title} at {self.send_time}"
