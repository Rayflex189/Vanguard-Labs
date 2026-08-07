from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Count
from django.http import JsonResponse
from django.utils import timezone
from .models import Notification, NotificationPreference, NotificationCategory
from .forms import NotificationPreferenceForm

@login_required
def notification_list(request):
    """
    Display all notifications for the current user, with filtering.
    """
    notifications = Notification.objects.filter(recipient=request.user).select_related('category', 'sender')
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        notifications = notifications.filter(category__slug=category_slug)
    # Filter by read/unread
    read_filter = request.GET.get('read')
    if read_filter == 'unread':
        notifications = notifications.filter(is_read=False)
    elif read_filter == 'read':
        notifications = notifications.filter(is_read=True)

    # Pagination can be added later
    context = {
        'notifications': notifications,
        'categories': NotificationCategory.objects.filter(is_active=True),
        'current_category': category_slug,
        'read_filter': read_filter,
        'unread_count': Notification.objects.filter(recipient=request.user, is_read=False).count(),
    }
    return render(request, 'notifications/list.html', context)

@login_required
def notification_detail(request, pk):
    """
    Show a single notification and mark as read.
    """
    notification = get_object_or_404(Notification, recipient=request.user, pk=pk)
    if not notification.is_read:
        notification.mark_as_read()
    return render(request, 'notifications/detail.html', {'notification': notification})

@login_required
def notification_mark_read(request, pk):
    """Mark a single notification as read."""
    notification = get_object_or_404(Notification, recipient=request.user, pk=pk)
    notification.mark_as_read()
    if request.GET.get('redirect_to'):
        return redirect(request.GET['redirect_to'])
    return redirect('notifications:list')

@login_required
def notification_mark_all_read(request):
    """Mark all notifications as read."""
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True, read_at=timezone.now())
    messages.success(request, "All notifications marked as read.")
    return redirect('notifications:list')

@login_required
def notification_delete(request, pk):
    """Soft delete? We'll hard delete for simplicity; you can add a trash feature."""
    notification = get_object_or_404(Notification, recipient=request.user, pk=pk)
    notification.delete()
    messages.success(request, "Notification deleted.")
    return redirect('notifications:list')

@login_required
def unread_count_json(request):
    """Return unread count as JSON."""
    count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    return JsonResponse({'unread_count': count})

@login_required
def preferences_view(request):
    """Edit notification preferences per category."""
    preferences = NotificationPreference.objects.filter(user=request.user)
    categories = NotificationCategory.objects.filter(is_active=True)
    # Create missing preferences
    for cat in categories:
        NotificationPreference.objects.get_or_create(user=request.user, category=cat)
    if request.method == 'POST':
        form = NotificationPreferenceForm(request.POST, user=request.user)
        if form.is_valid():
            for pref in preferences:
                pref.email_enabled = form.cleaned_data.get(f'email_{pref.category.slug}', False)
                pref.push_enabled = form.cleaned_data.get(f'push_{pref.category.slug}', False)
                pref.in_app_enabled = form.cleaned_data.get(f'in_app_{pref.category.slug}', False)
                pref.save()
            messages.success(request, "Preferences updated.")
            return redirect('notifications:preferences')
    else:
        form = NotificationPreferenceForm(user=request.user)
    return render(request, 'notifications/preferences.html', {'form': form, 'preferences': preferences})

@login_required
def mark_related_action(request, pk, action):
    """Mark an action (accept/reject) on a notification."""
    notification = get_object_or_404(Notification, recipient=request.user, pk=pk)
    if notification.action_status != 'pending':
        messages.warning(request, "This notification has already been acted upon.")
        return redirect('notifications:list')
    if action in ['accepted', 'rejected']:
        notification.action_status = action
        notification.save(update_fields=['action_status'])
        messages.success(request, f"Action '{action}' recorded.")
    return redirect('notifications:list')
