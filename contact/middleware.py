# contact/decorators.py
from django.core.cache import cache
from django.http import HttpResponseTooManyRequests
from functools import wraps

def rate_limit(limit=3, window=60):  # 3 requests per minute per IP
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            ip = request.META.get('REMOTE_ADDR')
            key = f'contact_rate_limit:{ip}'
            count = cache.get(key, 0)
            if count >= limit:
                return HttpResponseTooManyRequests("Too many submissions. Please try again later.")
            cache.set(key, count + 1, window)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
