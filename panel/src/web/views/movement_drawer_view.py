from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from panel.src.web.access.require_scope import require_scope


@login_required
@require_scope("panel.read")
@require_scope("inventory.write")
@require_http_methods(["GET"])
def movement_drawer_partial(request):
    ctx = {
        "product_id": request.GET.get("product_id"),
        "type": request.GET.get("type") or "entry",
    }
    return render(request, "panel/partials/_movement_drawer.html", ctx)


@login_required
@require_scope("panel.read")
@require_scope("inventory.write")
@require_http_methods(["GET"])
def movement_confirm_partial(request):
    ctx = {
        "product_id": request.GET.get("product_id"),
        "type": request.GET.get("type"),
        "quantity": request.GET.get("quantity"),
        "counted_stock": request.GET.get("counted_stock"),
        "reason": request.GET.get("reason"),
    }
    return render(request, "panel/partials/_movement_confirm.html", ctx)
