from django.views.generic import ListView, DetailView
from .models import BlogPost, Tag, BlogCategory
from django.db.models import Q

class BlogListView(ListView):
    model = BlogPost
    template_name = 'pages/blog/list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        queryset = BlogPost.objects.filter(is_published=True)
        tag_slug = self.kwargs.get('tag_slug')
        cat_slug = self.kwargs.get('category_slug')
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
        if cat_slug:
            queryset = queryset.filter(categories__slug=cat_slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['categories'] = BlogCategory.objects.all()
        return context

class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'pages/blog/detail.html'
    context_object_name = 'post'

    def get_object(self):
        obj = super().get_object()
        # markdown conversion can be done in template with filter
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related'] = BlogPost.objects.filter(
            Q(categories__in=self.object.categories.all()) |
            Q(tags__in=self.object.tags.all())
        ).exclude(id=self.object.id).distinct()[:3]
        return context
