from typing import Any, Iterable
from django.db import transaction

from contact.models import Contact
from contact.modules.contacts.infrastructure.orm.contact_history_models import (
    ContactFactModel,
    ContactTagModel,
    ContactSkuStatModel,
    ContactReorderProfileModel,
)


def upsert_fact(contact_id: int, key: str, value_json: Any, source: str, confidence: float = 1.0) -> ContactFactModel:
    obj, _created = ContactFactModel.objects.update_or_create(
        contact_id=contact_id,
        key=key,
        defaults={
            "value_json": value_json,
            "source": source,
            "confidence": confidence,
        },
    )
    return obj


def get_facts_dict(contact_id: int) -> dict[str, Any]:
    qs = ContactFactModel.objects.filter(contact_id=contact_id)
    return {row.key: row.value_json for row in qs}


def has_facts(contact_id: int, keys: set[str]) -> bool:
    present = set(
        ContactFactModel.objects.filter(contact_id=contact_id, key__in=list(keys)).values_list("key", flat=True)
    )
    return keys.issubset(present)


def get_or_create_reorder_profile(contact_id: int) -> ContactReorderProfileModel:
    obj, _created = ContactReorderProfileModel.objects.get_or_create(contact_id=contact_id)
    return obj


@transaction.atomic
def upsert_stats_bulk(contact_id: int, payloads: Iterable[dict[str, Any]]) -> None:
    for p in payloads:
        sku = p["sku"]
        defaults = {
            "orders_count": p.get("orders_count", 0),
            "qty_total": p.get("qty_total", 0),
            "qty_last": p.get("qty_last", 0),
            "qty_avg": p.get("qty_avg", 0.0),
            "first_ordered_at": p.get("first_ordered_at"),
            "last_ordered_at": p.get("last_ordered_at"),
            "score": p.get("score", 0.0),
        }
        ContactSkuStatModel.objects.update_or_create(contact_id=contact_id, sku=sku, defaults=defaults)
