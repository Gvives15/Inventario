from datetime import timedelta, date, datetime
import os
from contact.shared.infrastructure.uow import UnitOfWork
from contact.modules.reorder.infrastructure.selectors import list_due_contacts
from contact.modules.reorder.domain.rules import has_active_proposed
from contact.modules.orders.application.commands.create_order_proposal_cmd import execute as create_order
from contact.modules.orders.application.queries.get_order_summary_q import execute as get_summary
from contact.modules.gateways.whatsapp_cloud.application.services.wa_outbound_service import send_safe_product_list, send_safe_text
from contact.modules.contacts.infrastructure.orm.contact_history_repo import get_or_create_reorder_profile
from contact.modules.contacts.infrastructure.orm.contact_history_models import ContactSkuStatModel
from contact.modules.contacts.application.queries.has_min_profile_q import has_min_profile_q
from contact.modules.messaging.infrastructure.orm.message_event_repo import was_event_processed, log_inbound
from contact.models import OrderModel


def execute(dry_run: bool = False, apply: bool = False, limit: int = 100) -> int:
    count = 0
    catalog_id = os.environ.get("WA_CATALOG_ID", "default_catalog_id")
    today = date.today()
    now = datetime.now()
    elegibles, reasons = list_due_contacts(today, now, limit=limit)
    for contact, _wa in elegibles:
        if has_active_proposed(contact.id):
            continue
        if dry_run:
            count += 1
            continue
        if apply:
            daily_key = f"reorder:{contact.id}:{today.strftime('%Y%m%d')}"
            if was_event_processed("reorder_engine", daily_key):
                continue
            oid = create_order(contact.whatsapp_id)
            summary = get_summary(oid)
            
            skus = []
            for item in summary.get("items", []):
                ref = item.get("product_ref", "")
                if ref.startswith("SKU:"):
                    skus.append(ref.split("SKU:", 1)[1])
                else:
                    skus.append(ref)
            
            if skus:
                has_confirmed = OrderModel.objects.filter(contact_id=contact.id, status="COMPLETED").exists()
                sku_stats_cnt = ContactSkuStatModel.objects.filter(contact_id=contact.id).count()
                min_ok = has_min_profile_q(contact.id)
                use_history = has_confirmed or sku_stats_cnt >= 5
                source = "BASE_FROM_HISTORY" if use_history else "NEW_TEMPLATE"
                profile = get_or_create_reorder_profile(contact.id)
                lc = profile.default_list_code if source == "NEW_TEMPLATE" else None
                send_safe_product_list(contact.whatsapp_id, catalog_id, skus, proposal_source=source, contact_id=contact.id, list_code=lc)
            else:
                msg = f"Propuesta #{oid}\n" + (summary.get("text") or "No pude armar tu reposición, te contacto")
                send_safe_text(contact.whatsapp_id, msg, meta={"error": "FAILED_EMPTY_CATALOG"})
                
            profile = get_or_create_reorder_profile(contact.id)
            if profile.cadence_days:
                profile.next_reorder_date = date.today() + timedelta(days=profile.cadence_days)
                profile.save(update_fields=["next_reorder_date", "updated_at"])
            log_inbound("reorder_engine", daily_key, contact.whatsapp_id or "", contact.id, "PROCESSED", {"reasons": reasons})
            count += 1
    return count
