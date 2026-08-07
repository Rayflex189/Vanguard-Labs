from .models import Testimonial

def featured_testimonials(request):
    return {
        'featured_testimonials': Testimonial.objects.filter(
            is_published=True, is_featured=True
        ).order_by('featured_order')[:5]
    }
