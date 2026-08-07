from django.urls import path
from .views import HomeView, global_search, robots_txt, maintenance_view
from django.conf import settings

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search/', global_search, name='global_search'),
    path('robots.txt', robots_txt, name='robots_txt'),
]

# If maintenance mode is enabled, override the home route with a maintenance page.
# We can add a conditional check in middleware, but here we add a separate URL.
if getattr(settings, 'ENABLE_MAINTENANCE_MODE', False):
    urlpatterns = [
        path('', maintenance_view, name='maintenance'),
    ] + urlpatterns
