from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Testimonial

class TestimonialListView(ListView):
    model = Testimonial
    template_name = 'testimonials/testimonial_list.html'
    context_object_name = 'testimonials'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().filter(is_published=True)
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(client_name__icontains=q) |
                Q(client_company__icontains=q) |
                Q(content__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # For featured carousel
        context['featured'] = Testimonial.objects.filter(is_published=True, is_featured=True).order_by('featured_order')
        return context

class TestimonialDetailView(DetailView):
    model = Testimonial
    template_name = 'testimonials/testimonial_detail.html'
    context_object_name = 'testimonial'

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)
