from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Service, ServiceCategory

class ServiceListView(ListView):
    model = Service
    template_name = 'services/service_list.html'
    context_object_name = 'services'
    paginate_by = 9

    def get_queryset(self):
        qs = super().get_queryset().filter(is_active=True)
        # Category filter
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            self.category = ServiceCategory.objects.get(slug=category_slug)
            qs = qs.filter(category=self.category)
        else:
            self.category = None
        # Search
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ServiceCategory.objects.all()
        context['current_category'] = getattr(self, 'category', None)
        return context

class ServiceDetailView(DetailView):
    model = Service
    template_name = 'services/service_detail.html'
    context_object_name = 'service'

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
