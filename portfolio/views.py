from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Project, Category, Technology

class PortfolioListView(ListView):
    model = Project
    template_name = 'portfolio/list.html'
    context_object_name = 'projects'
    paginate_by = 9

    def get_queryset(self):
        qs = super().get_queryset().filter(is_published=True)
        # Category filter
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            self.category = get_object_or_404(Category, slug=category_slug)
            qs = qs.filter(category=self.category)
        else:
            self.category = None
        # Search
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(client__icontains=q) |
                Q(technologies__name__icontains=q)
            ).distinct()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = getattr(self, 'category', None)
        context['search_query'] = self.request.GET.get('q', '')
        return context


class PortfolioDetailView(DetailView):
    model = Project
    template_name = 'portfolio/detail.html'
    context_object_name = 'project'

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Related projects (same category, excluding current)
        context['related_projects'] = Project.objects.filter(
            category=self.object.category,
            is_published=True
        ).exclude(id=self.object.id)[:4]
        # Next/previous navigation
        all_projects = Project.objects.filter(is_published=True).order_by('-completion_date')
        project_list = list(all_projects)
        try:
            idx = project_list.index(self.object)
            context['previous_project'] = project_list[idx - 1] if idx > 0 else None
            context['next_project'] = project_list[idx + 1] if idx < len(project_list) - 1 else None
        except ValueError:
            context['previous_project'] = None
            context['next_project'] = None
        return context


def autocomplete_projects(request):
    """
    JSON endpoint for instant search suggestions.
    """
    q = request.GET.get('q', '').strip()
    if not q:
        return JsonResponse([], safe=False)
    projects = Project.objects.filter(
        Q(title__icontains=q) |
        Q(description__icontains=q) |
        Q(client__icontains=q),
        is_published=True
    )[:10]
    data = [{
        'title': p.title,
        'url': p.get_absolute_url(),
        'cover': p.cover_image.url if p.cover_image else '',
        'category': p.category.name if p.category else ''
    } for p in projects]
    return JsonResponse(data, safe=False)
