from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods

from panel.src.web.access.require_scope import require_scope
from inventory.src.infrastructure.orm.models import Product
from inventory.src.application.queries.list_movements_q import execute as q_kardex


@login_required
@require_scope("panel.read")
@require_http_methods(["GET"])
def product_detail_page(request, product_id: int):
    p = get_object_or_404(Product, id=product_id)
    return render(request, "panel/product_detail.html", {"p": p})


@login_required
@require_scope("panel.read")
@require_http_methods(["GET"])
def kardex_partial(request, product_id: int):
    items = q_kardex(product_id, 50)
    return render(request, "panel/partials/_kardex.html", {"items": items})
