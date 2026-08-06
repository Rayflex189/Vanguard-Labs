from django.views.generic import TemplateView
from portfolio.models import Project
from services.models import Service
from team.models import TeamMember
from testimonials.models import Testimonial
from core.models import CompanyStat
from django.http import JsonResponse
from django.db.models import Q
from blog.models import BlogPost
from services.models import Service

def global_search(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        projects = Project.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))[:5]
        posts = BlogPost.objects.filter(Q(title__icontains=query) | Q(content__icontains=query), is_published=True)[:5]
        services = Service.objects.filter(Q(name__icontains=query) | Q(description__icontains=query), is_active=True)[:5]
        # you can add more models here
        results = list(projects) + list(posts) + list(services)
    data = [{'name': str(item), 'url': item.get_absolute_url()} for item in results]
    return JsonResponse(data, safe=False)


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
