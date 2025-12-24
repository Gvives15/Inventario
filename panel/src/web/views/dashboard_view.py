from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from panel.src.web.access.require_scope import require_scope

from inventory.src.application.queries.dashboard.summary_q import execute as q_summary
from inventory.src.application.queries.dashboard.activity_q import execute as q_activity
from inventory.src.application.queries.dashboard.alerts_q import execute as q_alerts
from inventory.src.application.queries.dashboard.top_products_q import execute as q_top

from inventory.src.infrastructure.orm.product_repo import list_products


@login_required
@require_scope("panel.read")
@require_http_methods(["GET"])
def dashboard_page(request):
    return render(request, "panel/dashboard.html")


@login_required
@require_scope("dashboard.summary")
@require_http_methods(["GET"])
def summary_partial(request):
    return render(request, "panel/partials/_summary.html", {"d": q_summary()})


@login_required
@require_scope("dashboard.activity")
@require_http_methods(["GET"])
def activity_partial(request):
    return render(request, "panel/partials/_activity.html", {"d": q_activity()})


@login_required
@require_scope("dashboard.alerts")
@require_http_methods(["GET"])
def alerts_partial(request):
    return render(request, "panel/partials/_alerts.html", {"d": q_alerts(10, 10)})


@login_required
@require_scope("dashboard.top")
@require_http_methods(["GET"])
def top_products_partial(request):
    return render(request, "panel/partials/_top_products.html", {"d": q_top(10)})


@login_required
@require_scope("dashboard.search")
@require_http_methods(["GET"])
def search_results_partial(request):
    q = (request.GET.get("q") or "").strip()
    items = []
    if q:
        qs = list_products(search=q, category=None)[:10]
        items = [{"id": p.id, "sku": p.sku, "name": p.name, "stock_current": p.stock_current} for p in qs]
    return render(request, "panel/partials/_search_results.html", {"q": q, "items": items})
