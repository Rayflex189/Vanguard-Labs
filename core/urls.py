# core/urls.py
from django.urls import path
from django.http import HttpResponse
from .views import HomeView, global_search

app_name = 'core'

def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /admin/",
        "Disallow: /dashboard/",
        "Allow: /",
        "Sitemap: https://yourdomain.com/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

urlpatterns = [
    # Homepage
    path('', HomeView.as_view(), name='home'),

    # Global search (returns JSON)
    path('search/', global_search, name='global_search'),

    # robots.txt
    path('robots.txt', robots_txt, name='robots_txt'),
]
