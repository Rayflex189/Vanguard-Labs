from .models import SiteSettings

def site_settings(request):
    """
    Injects site settings into all templates.
    """
    try:
        settings = SiteSettings.objects.first()
    except:
        settings = None
    return {'site_settings': settings}

def maintenance_mode(request):
    """
    Injects maintenance mode flag.
    """
    from django.conf import settings
    return {'MAINTENANCE_MODE': getattr(settings, 'ENABLE_MAINTENANCE_MODE', False)}
