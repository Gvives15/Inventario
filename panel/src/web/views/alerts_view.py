from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from panel.src.web.access.require_scope import require_scope
from inventory.src.application.queries.dashboard.alerts_q import execute as q_alerts


@login_required
@require_scope("panel.read")
@require_scope("alerts.read")
@require_http_methods(["GET"])
def alerts_page(request):
    return render(request, "panel/alerts.html")


@login_required
@require_scope("panel.read")
@require_scope("alerts.read")
@require_http_methods(["GET"])
def alerts_list_partial(request):
    tab = (request.GET.get("tab") or "low").strip()
    d = q_alerts(20, 20)
    from panel.src.web.access.require_scope import ROLE_SCOPES
    user_groups = set(g.name.lower() for g in request.user.groups.all())
    can_write = any("inventory.write" in ROLE_SCOPES.get(g, set()) for g in user_groups) or request.user.is_superuser
    return render(request, "panel/partials/_alerts_tab.html", {"tab": tab, "d": d, "can_write": can_write})
