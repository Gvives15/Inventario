from datetime import date, datetime
from typing import Iterable, Tuple, List, Dict
from contact.models import Contact
from contact.modules.contacts.infrastructure.orm.contact_history_models import ContactReorderProfileModel
from django.utils import timezone as tz


def list_due_contacts(today: date, now: datetime, limit: int = 100) -> Tuple[List[Tuple[Contact, str]], Dict[str, int]]:
    qs = ContactReorderProfileModel.objects.filter(
        status=ContactReorderProfileModel.STATUS_ACTIVE,
        next_reorder_date__lte=today,
        cadence_days__gt=0,
    )
    contacts = Contact.objects.filter(id__in=qs.values_list("contact_id", flat=True))
    profiles = {p.contact_id: p for p in qs}
    reasons: Dict[str, int] = {"active_proposed": 0, "postpone_pending": 0, "postpone_until_future": 0}
    elegibles: List[Tuple[Contact, str]] = []
    from contact.modules.reorder.domain.rules import has_active_proposed
    for c in contacts[:limit]:
        p = profiles.get(c.id)
        if not c.whatsapp_id:
            continue
        if has_active_proposed(c.id):
            reasons["active_proposed"] += 1
            continue
        if p and p.postpone_status == ContactReorderProfileModel.POSTPONE_PENDING:
            reasons["postpone_pending"] += 1
            continue
        if p and p.postpone_status == ContactReorderProfileModel.POSTPONE_APPLIED and p.postpone_until_dt:
            until = p.postpone_until_dt
            if tz.is_naive(until):
                until = tz.make_aware(until)
            if until > tz.make_aware(now) if tz.is_naive(now) else now:
                reasons["postpone_until_future"] += 1
                continue
        elegibles.append((c, c.whatsapp_id))
    return elegibles, reasons
