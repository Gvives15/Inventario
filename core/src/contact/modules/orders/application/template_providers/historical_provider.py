from contact.modules.contacts.infrastructure.orm.contact_history_models import ContactSkuStatModel

def get_items(contact_id: int):
    # Get top 15 items by frequency (orders_count)
    stats = ContactSkuStatModel.objects.filter(contact_id=contact_id).order_by("-orders_count", "-last_ordered_at")[:15]
    
    items = []
    for s in stats:
        # Use avg qty, rounded to nearest integer, min 1
        qty = int(round(s.qty_avg))
        if qty < 1: 
            qty = 1
            
        items.append({
            "product_ref": s.sku, # stored as SKU in stats, but order needs SKU:xxx or just xxx? 
                                  # OrderItemModel stores product_ref. 
                                  # In refresh_stats we stored item.product_ref.
                                  # So we just pass it back.
            "qty": qty
        })
        
    return items
