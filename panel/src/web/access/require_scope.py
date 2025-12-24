from functools import wraps
from django.http import HttpResponseForbidden


def require_scope(scope_name: str):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Not authenticated")
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator
