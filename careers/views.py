# careers/views.py
from django.views.generic import ListView, DetailView
from .models import JobOpening

class JobListView(ListView):
    model = JobOpening
    template_name = 'careers/list.html'
    context_object_name = 'jobs'
    queryset = JobOpening.objects.filter(is_active=True)

class JobDetailView(DetailView):
    model = JobOpening
    template_name = 'careers/detail.html'
    context_object_name = 'job'
