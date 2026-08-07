from django.urls import path
from .views import (
    EventListView, EventDetailView, register_for_event,
    calendar_data
)

app_name = 'events'

urlpatterns = [
    path('', EventListView.as_view(), name='list'),
    path('category/<slug:category_slug>/', EventListView.as_view(), name='category'),
    path('calendar/data/', calendar_data, name='calendar_data'),
    path('<slug:slug>/', EventDetailView.as_view(), name='detail'),
    path('<slug:slug>/register/', register_for_event, name='register'),
]
