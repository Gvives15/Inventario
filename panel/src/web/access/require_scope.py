from functools import wraps
from django.http import HttpResponseForbidden


ROLE_SCOPES = {
    "admin": {
        "panel.read",
        "inventory.read",
        "inventory.write",
        "alerts.read",
        "movements.read",
        "user.admin",
        "dashboard.summary",
        "dashboard.activity",
        "dashboard.alerts",
        "dashboard.top",
        "dashboard.search",
    },
    "operador": {
        "panel.read",
        "inventory.read",
        "inventory.write",
        "alerts.read",
        "movements.read",
    },
    "auditor": {
        "panel.read",
        "inventory.read",
        "alerts.read",
        "movements.read",
    },
}


def require_scope(scope_name: str):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                return HttpResponseForbidden("Not authenticated")
            # Admin staff siempre puede ver Configuración
            if scope_name == "user.admin" and not (user.is_staff or user.is_superuser):
                return HttpResponseForbidden("Forbidden")
            # Validar por grupos
            user_groups = set(g.name.lower() for g in user.groups.all())
            allowed = False
            for g in user_groups:
                scopes = ROLE_SCOPES.get(g, set())
                if scope_name in scopes:
                    allowed = True
                    break
            # Superuser pasa siempre
            if user.is_superuser:
                allowed = True
            if not allowed:
                return HttpResponseForbidden("Forbidden")
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator
