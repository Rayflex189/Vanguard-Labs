# careers/urls.py
from django.urls import path
from .views import JobListView, JobDetailView

app_name = 'careers'
urlpatterns = [
    path('', JobListView.as_view(), name='list'),
    path('<slug:slug>/', JobDetailView.as_view(), name='detail'),
]
