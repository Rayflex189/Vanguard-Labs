from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Accounts (authentication)
    path('accounts/', include('accounts.urls')),

    # Analytics (dashboard + tracking)
    path('analytics/', include('analytics.urls')),

    # Blog
    path('blog/', include('blog.urls')),

    # Careers
    path('careers/', include('careers.urls')),

    # Clients
    path('clients/', include('clients.urls')),

    # Contact
    path('contact/', include('contact.urls')),

    # CRM
    path('crm/', include('crm.urls')),

    # Events
    path('events/', include('events.urls')),

    # Knowledge Base
    path('knowledgebase/', include('knowledgebase.urls')),

    # Messaging
    path('messages/', include('messaging.urls')),

    # Notifications
    path('notifications/', include('notifications.urls')),

    # Portfolio
    path('portfolio/', include('portfolio.urls')),

    # Projects Management
    path('projects/', include('projects_management.urls')),

    # Proposals
    path('proposals/', include('proposals.urls')),

    # Services
    path('services/', include('services.urls')),

    # Team
    path('team/', include('team.urls')),

    # Testimonials
    path('testimonials/', include('testimonials.urls')),

    # Core (homepage, search, robots.txt) – placed near the end
    path('', include('core.urls')),

    # CMS – catch‑all for static pages (must be last)
    path('', include('cms.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
