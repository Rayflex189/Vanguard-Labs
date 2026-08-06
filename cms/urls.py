# cms/urls.py
from django.urls import path
from .views import PageDetailView

app_name = 'cms'
urlpatterns = [
    path('<slug:slug>/', PageDetailView.as_view(), name='page'),
]
