from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from panel.src.web.access.require_scope import require_scope
from inventory.src.infrastructure.orm.product_repo import list_products
from inventory.src.application.queries.last_movement_q import execute as q_last


def _badge_for(p):
    if p.stock_current <= 0:
        return "sin"
    if p.stock_current <= (p.stock_minimum or 0):
        return "bajo"
    return "ok"


@login_required
@require_scope("panel.read")
@require_scope("inventory.read")
@require_http_methods(["GET"])
def products_page(request):
    return render(request, "panel/products.html")


@login_required
@require_scope("panel.read")
@require_scope("inventory.read")
@require_http_methods(["GET"])
def products_table_partial(request):
    search = (request.GET.get("q") or "").strip()
    category = (request.GET.get("category") or None) or None
    items = list_products(search=search or None, category=category)
    rows = []
    for p in items[:50]:
        last = q_last(p.id)
        rows.append({
            "id": p.id,
            "sku": p.sku,
            "name": p.name,
            "stock_current": p.stock_current,
            "stock_minimum": p.stock_minimum,
            "badge": _badge_for(p),
            "last_movement": last,
        })
    from panel.src.web.access.require_scope import ROLE_SCOPES
    user_groups = set(g.name.lower() for g in request.user.groups.all())
    can_write = any("inventory.write" in ROLE_SCOPES.get(g, set()) for g in user_groups) or request.user.is_superuser
    return render(request, "panel/partials/_products_table.html", {"items": rows, "q": search, "can_write": can_write})


@login_required
@require_scope("panel.read")
@require_scope("inventory.read")
@require_http_methods(["GET"])
def product_sheet_partial(request, product_id: int):
    from inventory.src.infrastructure.orm.models import Product
    p = Product.objects.filter(id=product_id).first()
    return render(request, "panel/partials/_product_sheet.html", {"product_id": product_id, "p": p})
