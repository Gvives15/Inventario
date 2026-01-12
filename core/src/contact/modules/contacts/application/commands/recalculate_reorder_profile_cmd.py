from django.db.models import Max
from contact.shared.infrastructure.uow import UnitOfWork
from contact.modules.contacts.infrastructure.orm.contact_history_models import ContactReorderProfileModel
from datetime import timedelta

def recalculate_reorder_profile_cmd(contact_id: int):
    with UnitOfWork() as uow:
        # 1. Get last 5 confirmed orders to calculate cadence
        orders = uow.orders.get_confirmed_by_contact(contact_id)
        # Sort by date
        orders = sorted(orders, key=lambda x: x.created_at)
        
        if len(orders) < 2:
            return # Not enough data
            
        # Calculate intervals
        intervals = []
        for i in range(1, len(orders)):
            delta = orders[i].created_at - orders[i-1].created_at
            intervals.append(delta.days)
            
        if not intervals:
            return

        avg_interval = sum(intervals) / len(intervals)
        cadence = int(round(avg_interval))
        
        last_order_date = orders[-1].created_at.date()
        next_date = last_order_date + timedelta(days=cadence)
        
        # Upsert profile
        profile, _ = ContactReorderProfileModel.objects.get_or_create(contact_id=contact_id)
        profile.cadence_days = cadence
        profile.next_reorder_date = next_date
        profile.save()
        
        return profile
