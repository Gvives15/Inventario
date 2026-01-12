from collections import defaultdict
from typing import Any
from django.utils import timezone

from contact.models import OrderModel, OrderItemModel
from contact.modules.contacts.domain.rules import is_valid_sku_for_stats
from contact.modules.contacts.infrastructure.orm.contact_history_repo import upsert_stats_bulk


def refresh_contact_sku_stats_cmd(contact_id: int) -> None:
    orders = OrderModel.objects.filter(contact_id=contact_id, status="CONFIRMED").values_list("id", "updated_at")
    order_updated_map = {oid: ts for oid, ts in orders}
    if not order_updated_map:
        return

    items = OrderItemModel.objects.filter(order_id__in=list(order_updated_map.keys())).values(
        "order_id", "product_ref", "qty"
    )

    agg = defaultdict(lambda: {"orders": set(), "qty_total": 0, "last_ts": None, "last_qty": 0, "first_ts": None})
    for it in items:
        sku = str(it["product_ref"])
        if not is_valid_sku_for_stats(sku):
            continue
        oid = int(it["order_id"])
        qty = int(it["qty"])
        ts = order_updated_map.get(oid)
        a = agg[sku]
        a["orders"].add(oid)
        a["qty_total"] += qty
        if a["first_ts"] is None or (ts and ts < a["first_ts"]):
            a["first_ts"] = ts
        if a["last_ts"] is None or (ts and ts > a["last_ts"]):
            a["last_ts"] = ts
            a["last_qty"] = qty

    payloads = []
    for sku, a in agg.items():
        orders_count = len(a["orders"])
        qty_total = a["qty_total"]
        qty_avg = float(qty_total) / float(orders_count) if orders_count > 0 else 0.0
        payloads.append(
            {
                "sku": sku,
                "orders_count": orders_count,
                "qty_total": qty_total,
                "qty_last": a["last_qty"],
                "qty_avg": qty_avg,
                "first_ordered_at": a["first_ts"],
                "last_ordered_at": a["last_ts"],
                "score": 0.0,
            }
        )

    if payloads:
        upsert_stats_bulk(contact_id, payloads)
