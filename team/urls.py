from django.urls import path
from .views import TeamListView, TeamDetailView

app_name = 'team'

urlpatterns = [
    path('', TeamListView.as_view(), name='list'),
    path('role/<slug:role_slug>/', TeamListView.as_view(), name='role'),
    path('<slug:slug>/', TeamDetailView.as_view(), name='detail'),
]
