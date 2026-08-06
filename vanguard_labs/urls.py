from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),           # home, etc.
    path('portfolio/', include('portfolio.urls')),
    path('services/', include('services.urls')),
    path('team/', include('team.urls')),
    path('testimonials/', include('testimonials.urls')),
    path('blog/', include('blog.urls')),
    path('contact/', include('contact.urls')),
    path('careers/', include('careers.urls')),
    path('cms/', include('cms.urls')),
    path('events/', include('events.urls')),
    path('knowledgebase/', include('knowledgebase.urls')),
    path('messages/', include('messaging.urls')),
    path('notifications/', include('notifications.urls')),
    path('projects/', include('projects_management.urls')),
    path('proposals/', include('proposals.urls')),
    # Add others as needed
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
