from django import template
from django.template.loader import render_to_string
from ..models import Menu, SiteConfig

register = template.Library()

@register.simple_tag(takes_context=True)
def render_menu(context, menu_slug, template='cms/menu.html'):
    """
    Render a menu by its slug.
    Usage: {% render_menu 'main-menu' %}
    """
    try:
        menu = Menu.objects.prefetch_related('items').get(slug=menu_slug)
        request = context.get('request')
        return render_to_string(template, {'menu': menu, 'request': request})
    except Menu.DoesNotExist:
        return ''

@register.simple_tag
def get_site_config():
    """
    Returns the SiteConfig instance.
    Usage: {% get_site_config as config %}
    """
    return SiteConfig.objects.first()
