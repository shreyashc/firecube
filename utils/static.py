import re
from urllib.parse import urlsplit

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import re_path
from django.views.static import serve


def serve_wrap(*args ,**kwargs):
    response = serve(*args ,**kwargs)
    response['Content-Disposition'] = 'attachment;'
    response['X-Content-Type-Options'] = 'nosniff;'
    return response

def static(prefix, view = serve_wrap, **kwargs):
    if not prefix:
        raise ImproperlyConfigured("Empty static prefix not permitted")
    return [
        re_path(r'^%s(?P<path>.*)$' % re.escape(prefix.lstrip('/')), view, kwargs=kwargs),
    ]