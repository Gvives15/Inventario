from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from panel.src.web.access.require_scope import require_scope
from inventory.src.application.queries.movements_q import list_movements

@login_required
@require_scope("panel.read")
@require_scope("movements.read")
def movements_page(request):
    return render(request, "panel/movements.html", {})

@login_required
@require_scope("panel.read")
@require_scope("movements.read")
@require_http_methods(["GET"])
def movements_list_partial(request):
    range_opt = (request.GET.get("range") or "").strip()
    days = None
    if range_opt == "today":
        days = 1
    elif range_opt == "7d":
        days = 7
    sku = (request.GET.get("sku") or "").strip()
    movement_type = (request.GET.get("type") or "").strip() or None
    items = list_movements(days=days, sku=sku or None, movement_type=movement_type or None)
    return render(request, "panel/partials/_movements_list.html", {"items": items})
