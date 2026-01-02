from django.utils import timezone
from django.db.models import Sum, Count
from inventory.infrastructure.orm.models import StockMovement


def execute():
    now = timezone.now()
    start_today = now.replace(hour=0, minute=0, second=0, microsecond=0)

    qs = StockMovement.objects.filter(created_at__gte=start_today)

    entry = qs.filter(movement_type=StockMovement.TYPE_ENTRY).aggregate(
        units=Sum("delta"),
        count=Count("id"),
    )

    exit_agg = qs.filter(movement_type=StockMovement.TYPE_EXIT).aggregate(
        units=Sum("delta"),
        count=Count("id"),
    )

    adjust = qs.filter(movement_type=StockMovement.TYPE_ADJUST).aggregate(
        units=Sum("delta"),
        count=Count("id"),
    )

    entry_units = int(entry["units"] or 0)
    entry_count = int(entry["count"] or 0)

    exit_units = int(-(exit_agg["units"] or 0))
    exit_count = int(exit_agg["count"] or 0)

    adjust_units = int(adjust["units"] or 0)
    adjust_count = int(adjust["count"] or 0)

    return {
        "entry_units": entry_units,
        "entry_count": entry_count,
        "exit_units": exit_units,
        "exit_count": exit_count,
        "adjust_units": adjust_units,
        "adjust_count": adjust_count,
    }
