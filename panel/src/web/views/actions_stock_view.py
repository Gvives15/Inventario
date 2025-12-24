from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from panel.src.web.access.require_scope import require_scope

from inventory.src.domain.errors import InventoryError
from inventory.src.application.commands.record_entry_cmd import execute as cmd_entry
from inventory.src.application.commands.record_exit_cmd import execute as cmd_exit
from inventory.src.application.commands.adjust_to_count_cmd import execute as cmd_adjust_to_count
from inventory.src.domain.rules import normalize_sku
from inventory.src.infrastructure.orm.models import Product


def _msg(request, text: str, ok: bool, status: int):
    level = "ok" if ok else "bad"
    resp = render(request, "panel/partials/_toast.html", {"level": level, "message": text}, status=status)
    if ok:
        resp["HX-Trigger"] = "inventory:changed"
    return resp


@login_required
@require_scope("panel.read")
@require_scope("inventory.write")
@require_http_methods(["POST"])
def stock_entry_submit(request):
    try:
        product_id = int(request.POST.get("product_id", ""))
        quantity = int(request.POST.get("quantity", ""))
        reason = (request.POST.get("reason") or "").strip()
        cmd_entry(product_id, quantity, reason, request.user)
        return _msg(request, "Entrada registrada ✅", True, 200)
    except (ValueError, KeyError):
        return _msg(request, "Datos inválidos", False, 400)
    except InventoryError as e:
        return _msg(request, str(e), False, 400)


@login_required
@require_scope("panel.read")
@require_scope("inventory.write")
@require_http_methods(["POST"])
def stock_exit_submit(request):
    try:
        product_id = int(request.POST.get("product_id", ""))
        quantity = int(request.POST.get("quantity", ""))
        reason = (request.POST.get("reason") or "").strip()
        cmd_exit(product_id, quantity, reason, request.user)
        return _msg(request, "Salida registrada ✅", True, 200)
    except (ValueError, KeyError):
        return _msg(request, "Datos inválidos", False, 400)
    except InventoryError as e:
        return _msg(request, str(e), False, 400)


@login_required
@require_scope("panel.read")
@require_scope("inventory.write")
@require_http_methods(["POST"])
def stock_adjust_to_count_submit(request):
    try:
        product_id = int(request.POST.get("product_id", ""))
        counted_stock = int(request.POST.get("counted_stock", ""))
        reason = (request.POST.get("reason") or "").strip()
        cmd_adjust_to_count(product_id, counted_stock, reason, request.user)
        return _msg(request, "Ajuste aplicado ✅", True, 200)
    except (ValueError, KeyError):
        return _msg(request, "Datos inválidos", False, 400)
    except InventoryError as e:
        return _msg(request, str(e), False, 400)


@login_required
@require_scope("panel.read")
@require_scope("inventory.write")
@require_http_methods(["POST"])
def stock_entry_by_sku_submit(request):
    raw_sku = request.POST.get("sku", "")
    quantity = int(request.POST["quantity"]) 
    reason = (request.POST.get("reason") or "").strip()
    try:
        sku = normalize_sku(raw_sku)
        p = Product.objects.filter(sku=sku).first()
        if not p:
            return _msg(request, "SKU no encontrado", False, 404)
        cmd_entry(p.id, quantity, reason, request.user)
        return _msg(request, "Entrada registrada ✅", True, 200)
    except InventoryError as e:
        return _msg(request, str(e), False, 400)


@login_required
@require_scope("panel.read")
@require_scope("inventory.write")
@require_http_methods(["POST"])
def stock_exit_by_sku_submit(request):
    raw_sku = request.POST.get("sku", "")
    quantity = int(request.POST["quantity"]) 
    reason = (request.POST.get("reason") or "").strip()
    try:
        sku = normalize_sku(raw_sku)
        p = Product.objects.filter(sku=sku).first()
        if not p:
            return _msg(request, "SKU no encontrado", False, 404)
        cmd_exit(p.id, quantity, reason, request.user)
        return _msg(request, "Salida registrada ✅", True, 200)
    except InventoryError as e:
        return _msg(request, str(e), False, 400)


@login_required
@require_scope("panel.read")
@require_scope("inventory.write")
@require_http_methods(["POST"])
def stock_adjust_to_count_by_sku_submit(request):
    raw_sku = request.POST.get("sku", "")
    counted_stock = int(request.POST["counted_stock"]) 
    reason = (request.POST.get("reason") or "").strip()
    try:
        sku = normalize_sku(raw_sku)
        p = Product.objects.filter(sku=sku).first()
        if not p:
            return _msg(request, "SKU no encontrado", False, 404)
        cmd_adjust_to_count(p.id, counted_stock, reason, request.user)
        return _msg(request, "Ajuste aplicado ✅", True, 200)
    except InventoryError as e:
        return _msg(request, str(e), False, 400)
