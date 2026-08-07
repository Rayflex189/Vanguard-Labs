from django.urls import path
from .views import (
    notification_list, notification_detail, notification_mark_read,
    notification_mark_all_read, notification_delete, unread_count_json,
    preferences_view, mark_related_action
)

app_name = 'notifications'

urlpatterns = [
    path('', notification_list, name='list'),
    path('unread/', unread_count_json, name='unread_count'),
    path('preferences/', preferences_view, name='preferences'),
    path('<uuid:pk>/', notification_detail, name='detail'),
    path('<uuid:pk>/mark-read/', notification_mark_read, name='mark_read'),
    path('mark-all-read/', notification_mark_all_read, name='mark_all_read'),
    path('<uuid:pk>/delete/', notification_delete, name='delete'),
    path('<uuid:pk>/action/<str:action>/', mark_related_action, name='action'),
]
