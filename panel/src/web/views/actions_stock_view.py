from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from panel.src.web.access.require_scope import require_scope

from inventory.src.domain.errors import InventoryError
from inventory.src.application.commands.record_entry_cmd import execute as cmd_entry
from inventory.src.application.commands.record_exit_cmd import execute as cmd_exit
from inventory.src.application.commands.adjust_to_count_cmd import execute as cmd_adjust_to_count


def _msg(text: str, ok: bool, status: int):
    cls = "ok" if ok else "bad"
    return HttpResponse(f'<div class="{cls}"><strong>{text}</strong></div>', status=status)


@login_required
@require_scope("inventory.write")
@require_http_methods(["POST"])
def stock_entry_submit(request):
    product_id = int(request.POST["product_id"]) 
    quantity = int(request.POST["quantity"]) 
    reason = (request.POST.get("reason") or "").strip()
    try:
        cmd_entry(product_id, quantity, reason, request.user)
        return _msg("Entrada registrada ✅", True, 200)
    except InventoryError as e:
        return _msg(str(e), False, 400)


@login_required
@require_scope("inventory.write")
@require_http_methods(["POST"])
def stock_exit_submit(request):
    product_id = int(request.POST["product_id"]) 
    quantity = int(request.POST["quantity"]) 
    reason = (request.POST.get("reason") or "").strip()
    try:
        cmd_exit(product_id, quantity, reason, request.user)
        return _msg("Salida registrada ✅", True, 200)
    except InventoryError as e:
        return _msg(str(e), False, 400)


@login_required
@require_scope("inventory.write")
@require_http_methods(["POST"])
def stock_adjust_to_count_submit(request):
    product_id = int(request.POST["product_id"]) 
    counted_stock = int(request.POST["counted_stock"]) 
    reason = (request.POST.get("reason") or "").strip()
    try:
        cmd_adjust_to_count(product_id, counted_stock, reason, request.user)
        return _msg("Ajuste aplicado ✅", True, 200)
    except InventoryError as e:
        return _msg(str(e), False, 400)
