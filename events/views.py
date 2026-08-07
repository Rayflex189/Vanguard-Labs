from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Event, EventRegistration, EventCategory, Venue
from .forms import EventRegistrationForm

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 9

    def get_queryset(self):
        qs = super().get_queryset().filter(status='published')
        # Filter by category
        cat_slug = self.kwargs.get('category_slug')
        if cat_slug:
            qs = qs.filter(category__slug=cat_slug)
        # Search
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(venue__name__icontains=q)
            )
        # Filter by upcoming/past
        timeframe = self.request.GET.get('timeframe')
        now = timezone.now()
        if timeframe == 'upcoming':
            qs = qs.filter(start_date__gte=now)
        elif timeframe == 'past':
            qs = qs.filter(end_date__lt=now)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = EventCategory.objects.all()
        context['current_category'] = self.kwargs.get('category_slug')
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_registered'] = False
        if self.request.user.is_authenticated:
            context['is_registered'] = self.object.registrations.filter(
                user=self.request.user,
                status__in=['confirmed', 'attended']
            ).exists()
        context['registration_form'] = EventRegistrationForm()
        return context


@login_required
def register_for_event(request, slug):
    event = get_object_or_404(Event, slug=slug, status='published')
    if not event.registration_open:
        messages.error(request, "Registration for this event is closed.")
        return redirect('events:detail', slug=slug)

    # Check if already registered
    existing = event.registrations.filter(email=request.user.email)
    if existing.exists():
        messages.warning(request, "You are already registered for this event.")
        return redirect('events:detail', slug=slug)

    # Check capacity
    if event.max_attendees:
        current_count = event.registrations.filter(status__in=['confirmed', 'pending']).count()
        if current_count >= event.max_attendees:
            messages.error(request, "This event is fully booked.")
            return redirect('events:detail', slug=slug)

    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.event = event
            registration.user = request.user
            registration.email = request.user.email
            registration.full_name = request.user.get_full_name() or request.user.username
            registration.status = 'confirmed' if event.is_free else 'pending'
            registration.save()
            messages.success(request, f"Successfully registered for {event.title}!")
            # Send confirmation email
            send_registration_confirmation(request, event, registration)
            return redirect('events:detail', slug=slug)
    else:
        form = EventRegistrationForm(initial={
            'email': request.user.email,
            'full_name': request.user.get_full_name() or request.user.username,
        })
    return render(request, 'events/register_form.html', {'event': event, 'form': form})


def send_registration_confirmation(request, event, registration):
    """Send confirmation email to registrant."""
    subject = f"Registration Confirmation: {event.title}"
    context = {
        'event': event,
        'registration': registration,
        'site_name': settings.SITE_NAME or 'Vanguard Labs',
        'protocol': 'https' if request.is_secure() else 'http',
        'domain': request.get_host(),
    }
    html_body = render_to_string('events/email_registration_confirmation.html', context)
    plain_body = render_to_string('events/email_registration_confirmation.txt', context)
    send_mail(
        subject=subject,
        message=plain_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[registration.email],
        html_message=html_body,
        fail_silently=True,
    )


def calendar_data(request):
    """
    JSON endpoint for FullCalendar or similar.
    Returns events in the requested month.
    """
    events = Event.objects.filter(status='published')
    # Optionally filter by date range from request
    start_str = request.GET.get('start')
    end_str = request.GET.get('end')
    if start_str and end_str:
        events = events.filter(start_date__gte=start_str, end_date__lte=end_str)

    data = []
    for event in events:
        data.append({
            'id': event.id,
            'title': event.title,
            'start': event.start_date.isoformat(),
            'end': event.end_date.isoformat(),
            'url': event.get_absolute_url(),
            'color': '#3B82F6',  # Blue
            'allDay': False,
        })
    return JsonResponse(data, safe=False)
