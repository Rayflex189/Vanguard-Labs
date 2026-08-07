from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView
from django.db.models import Q
from django.conf import settings
from django.core.cache import cache

from portfolio.models import Project
from services.models import Service
from team.models import TeamMember
from testimonials.models import Testimonial
from blog.models import BlogPost
from .models import CompanyStat, FAQ


class HomeView(TemplateView):
    """
    Homepage with all sections.
    """
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Featured projects (for portfolio showcase)
        context['featured_projects'] = Project.objects.filter(featured=True).order_by('-completion_date')[:6]
        # Services
        context['services'] = Service.objects.filter(is_active=True).order_by('order')
        # Team members (limit to 8)
        context['team'] = TeamMember.objects.all().order_by('order')[:8]
        # Testimonials (shuffle for variety)
        context['testimonials'] = Testimonial.objects.filter(is_published=True).order_by('?')[:5]
        # Stats
        context['stats'] = CompanyStat.objects.all().order_by('order')
        # FAQs (optional)
        context['faqs'] = FAQ.objects.filter(is_published=True).order_by('order')[:6]
        return context


def global_search(request):
    """
    JSON endpoint for instant global search.
    Returns suggestions for projects, blog posts, services, team members.
    """
    query = request.GET.get('q', '').strip()
    results = []

    if query:
        # Search projects
        projects = Project.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )[:4]
        for p in projects:
            results.append({
                'type': 'project',
                'name': p.title,
                'url': p.get_absolute_url(),
                'category': 'Portfolio'
            })

        # Search blog posts
        posts = BlogPost.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            is_published=True
        )[:4]
        for p in posts:
            results.append({
                'type': 'blog',
                'name': p.title,
                'url': p.get_absolute_url(),
                'category': 'Blog'
            })

        # Search services
        services = Service.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query),
            is_active=True
        )[:3]
        for s in services:
            results.append({
                'type': 'service',
                'name': s.name,
                'url': s.get_absolute_url(),
                'category': 'Service'
            })

        # Search team members
        team = TeamMember.objects.filter(
            Q(name__icontains=query) | Q(role__icontains=query) | Q(bio__icontains=query)
        )[:3]
        for t in team:
            results.append({
                'type': 'team',
                'name': t.name,
                'url': t.get_absolute_url(),
                'category': 'Team'
            })

    return JsonResponse(results, safe=False)


def robots_txt(request):
    """
    Dynamically generate robots.txt.
    """
    lines = [
        "User-Agent: *",
        "Disallow: /admin/",
        "Disallow: /dashboard/",
        "Disallow: /accounts/",
        "Allow: /",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def maintenance_view(request):
    """
    Maintenance mode page.
    """
    site_settings = SiteSettings.objects.first()
    message = site_settings.maintenance_message if site_settings else "We'll be back soon."
    return render(request, 'core/maintenance.html', {'message': message})
