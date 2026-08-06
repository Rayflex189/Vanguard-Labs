from .models import SiteConfig

def site_config(request):
    """
    Inject site configuration into every template context.
    """
    return {'site_config': SiteConfig.objects.first()}
