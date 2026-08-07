from django import template
from markdown import markdown
from django.utils.safestring import mark_safe
from django.utils.text import slugify
import re

register = template.Library()

@register.filter
def markdown_to_html(value):
    """Convert markdown to HTML."""
    if not value:
        return ''
    return mark_safe(markdown(value))

@register.filter
def truncate_chars(value, max_length=100):
    """Truncate a string by character count."""
    if len(value) <= max_length:
        return value
    return value[:max_length] + '...'

@register.simple_tag
def current_year():
    """Return current year."""
    from datetime import datetime
    return datetime.now().year

@register.filter
def add_class(field, css_class):
    """Add a CSS class to a form field."""
    return field.as_widget(attrs={'class': css_class})

@register.filter
def slugify_string(value):
    """Slugify a string."""
    return slugify(value)

@register.filter
def extract_first_paragraph(html):
    """Extract the first paragraph from HTML content."""
    if not html:
        return ''
    # Strip tags and get first paragraph
    clean = re.sub(r'<[^>]+>', '', html)
    paragraphs = clean.split('\n\n')
    if paragraphs:
        return paragraphs[0]
    return clean

@register.filter
def get_item(dictionary, key):
    """Get item from a dictionary."""
    return dictionary.get(key)
