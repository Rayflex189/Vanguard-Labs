from django.urls import path
from .views import TestimonialListView, TestimonialDetailView

app_name = 'testimonials'

urlpatterns = [
    path('', TestimonialListView.as_view(), name='list'),
    path('<int:pk>/', TestimonialDetailView.as_view(), name='detail'),
]
