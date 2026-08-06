from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView
from django.http import Http404
from .models import Page

class PageDetailView(DetailView):
    """
    Renders a single page based on its full path (slug hierarchy).
    """
    model = Page
    template_name = 'cms/page.html'  # fallback; will be overridden by page's template_name
    context_object_name = 'page'

    def get_object(self, queryset=None):
        path = self.kwargs.get('path', '')
        if not path:
            # Try to get the root page (parent is null)
            page = Page.objects.filter(parent__isnull=True, is_published=True).first()
            if page:
                return page
            raise Http404("No root page found.")
        # Split path into slugs
        slugs = path.split('/')
        page = None
        for slug in slugs:
            if page is None:
                # Root level
                page = get_object_or_404(Page, slug=slug, parent__isnull=True, is_published=True)
            else:
                page = get_object_or_404(Page, slug=slug, parent=page, is_published=True)
        return page

    def get_template_names(self):
        if self.object.template_name:
            return [self.object.template_name]
        return ['cms/page.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add breadcrumbs
        context['breadcrumbs'] = self.object.get_ancestors()
        return context


def page_not_found_view(request, exception=None):
    """
    Custom 404 that tries to show a CMS page with slug '404' if it exists.
    """
    try:
        page = Page.objects.get(slug='404', is_published=True, parent__isnull=True)
        return render(request, 'cms/page.html', {'page': page}, status=404)
    except Page.DoesNotExist:
        # fallback to default 404
        from django.views.defaults import page_not_found
        return page_not_found(request, exception)
