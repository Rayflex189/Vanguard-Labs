from django.views.generic import TemplateView
from portfolio.models import Project
from services.models import Service
from team.models import TeamMember
from testimonials.models import Testimonial
from core.models import CompanyStat

class HomeView(TemplateView):
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_projects'] = Project.objects.filter(featured=True)[:6]
        context['services'] = Service.objects.filter(is_active=True).order_by('order')
        context['team'] = TeamMember.objects.all().order_by('order')[:8]
        context['testimonials'] = Testimonial.objects.filter(is_published=True).order_by('?')
        context['stats'] = CompanyStat.objects.all().order_by('order')
        return context
