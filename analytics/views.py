from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import timedelta
import json

from .models import PageView, CustomEvent, DailyStats

# --- Dashboard (staff only) ---
@staff_member_required
def analytics_dashboard(request):
    """
    A simple dashboard showing key metrics.
    """
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    last_7_days = today - timedelta(days=7)

    # Basic stats
    total_views = PageView.objects.count()
    unique_visitors = PageView.objects.values('user').distinct().count() or PageView.objects.values('ip_address').distinct().count()
    total_events = CustomEvent.objects.count()
    avg_response = PageView.objects.filter(response_time__isnull=False).aggregate(avg=Avg('response_time'))['avg'] or 0

    # Recent 7-day trend
    views_by_day = PageView.objects.filter(timestamp__date__gte=last_7_days) \
                                    .values('timestamp__date') \
                                    .annotate(count=Count('id')) \
                                    .order_by('timestamp__date')

    events_by_day = CustomEvent.objects.filter(timestamp__date__gte=last_7_days) \
                                        .values('timestamp__date') \
                                        .annotate(count=Count('id')) \
                                        .order_by('timestamp__date')

    # Popular pages
    popular_pages = PageView.objects.values('path') \
                                    .annotate(count=Count('id')) \
                                    .order_by('-count')[:10]

    # Recent activity
    recent_views = PageView.objects.select_related('user')[:20]
    recent_events = CustomEvent.objects.select_related('user')[:20]

    context = {
        'total_views': total_views,
        'unique_visitors': unique_visitors,
        'total_events': total_events,
        'avg_response_time': round(avg_response, 2),
        'views_by_day': list(views_by_day),
        'events_by_day': list(events_by_day),
        'popular_pages': list(popular_pages),
        'recent_views': recent_views,
        'recent_events': recent_events,
    }
    return render(request, 'analytics/dashboard.html', context)


# --- Tracking endpoint (collect events) ---
@csrf_exempt
@require_POST
def track_event(request):
    """
    Accept JSON data to log a custom event.
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    # Extract data
    event_name = data.get('event_name')
    if not event_name:
        return JsonResponse({'error': 'event_name is required'}, status=400)

    # Build the event object
    event = CustomEvent(
        event_name=event_name,
        event_category=data.get('event_category'),
        event_label=data.get('event_label'),
        event_value=data.get('event_value'),
        page_path=data.get('page_path'),
        referer=data.get('referer'),
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT'),
    )
    if request.user.is_authenticated:
        event.user = request.user
    # optional session key
    if request.session.session_key:
        event.session_key = request.session.session_key

    event.save()
    return JsonResponse({'status': 'ok'}, status=201)


# --- Data API for charts (JSON) ---
@require_GET
def analytics_data(request):
    """
    Return analytics data as JSON for frontend charts.
    """
    days = int(request.GET.get('days', 30))
    start_date = timezone.now().date() - timedelta(days=days)

    views = PageView.objects.filter(timestamp__date__gte=start_date) \
                            .values('timestamp__date') \
                            .annotate(count=Count('id')) \
                            .order_by('timestamp__date')
    events = CustomEvent.objects.filter(timestamp__date__gte=start_date) \
                                .values('timestamp__date') \
                                .annotate(count=Count('id')) \
                                .order_by('timestamp__date')

    # Build a dict date -> {views, events}
    date_range = [start_date + timedelta(days=i) for i in range(days + 1)]
    result = {}
    for d in date_range:
        result[d.isoformat()] = {'views': 0, 'events': 0}

    for item in views:
        date_str = item['timestamp__date'].isoformat()
        if date_str in result:
            result[date_str]['views'] = item['count']
    for item in events:
        date_str = item['timestamp__date'].isoformat()
        if date_str in result:
            result[date_str]['events'] = item['count']

    return JsonResponse(result)


# --- Simple page tracking middleware is optional and not included here,
#     but can be added to capture every request automatically.
