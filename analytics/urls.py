from django.urls import path
from .views import analytics_dashboard, track_event, analytics_data

app_name = 'analytics'

urlpatterns = [
    path('dashboard/', analytics_dashboard, name='dashboard'),
    path('track/', track_event, name='track_event'),
    path('data/', analytics_data, name='data'),
]
