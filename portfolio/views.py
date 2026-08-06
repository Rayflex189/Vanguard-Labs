from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import Project, Category

class PortfolioListView(ListView):
    model = Project
    template_name = 'pages/portfolio/list.html'
    context_object_name = 'projects'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset().filter(featured=True)  # or all
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class PortfolioDetailView(DetailView):
    model = Project
    template_name = 'pages/portfolio/detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # related projects (same category, excluding current)
        context['related_projects'] = Project.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:3]
        return context
