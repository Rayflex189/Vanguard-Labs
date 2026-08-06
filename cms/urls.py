from django.urls import path, re_path
from .views import PageDetailView

app_name = 'cms'

urlpatterns = [
    # Catch-all for any path (including root)
    # The path is captured as a string. We'll handle root via the view.
    re_path(r'^(?P<path>.*)/?$', PageDetailView.as_view(), name='page'),
]
