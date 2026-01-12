from django.core.management.base import BaseCommand
from contact.models import Contact, OrderModel, OrderOpsEventModel
from contact.modules.orders.application.commands.change_ops_status_cmd import execute
from contact.modules.orders.domain.order_status import OrderStatus

class Command(BaseCommand):
    help = "Simula SOP-001: crea pedidos y ejecuta transiciones para validar la cola operativa"

    def handle(self, *args, **options):
        c, _ = Contact.objects.get_or_create(
            whatsapp_id="wa_sop",
            defaults={"name": "Cliente SOP", "zone": "Z", "business_type": "K", "type": Contact.TYPE_CLIENT}
        )
        # Limpiar órdenes previas de este test para evitar ruido
        OrderModel.objects.filter(contact=c).delete()
        
        orders = []
        # 2 normales confirmados
        o1 = OrderModel.objects.create(contact=c, status=OrderStatus.CONFIRMED.value, ops_status=OrderModel.OPS_CONFIRMED)
        o2 = OrderModel.objects.create(contact=c, status=OrderStatus.CONFIRMED.value, ops_status=OrderModel.OPS_CONFIRMED)
        # 1 review por SKU_UNKNOWN
        o3 = OrderModel.objects.create(contact=c, status=OrderStatus.CONFIRMED.value, ops_status=OrderModel.OPS_CONFIRMED)
        # 1 cancel post-confirm
        o4 = OrderModel.objects.create(contact=c, status=OrderStatus.CONFIRMED.value, ops_status=OrderModel.OPS_CONFIRMED)
        # 1 opcional segundo review
        o5 = OrderModel.objects.create(contact=c, status=OrderStatus.CONFIRMED.value, ops_status=OrderModel.OPS_CONFIRMED)
        orders.extend([o1, o2, o3, o4, o5])

        # Flujos
        def run_full_flow(o):
            execute(o.id, OrderModel.OPS_PREPARING)
            execute(o.id, OrderModel.OPS_READY)
            execute(o.id, OrderModel.OPS_OUT_FOR_DELIVERY)
            execute(o.id, OrderModel.OPS_DELIVERED)
            execute(o.id, OrderModel.OPS_PAID)

        run_full_flow(o1)
        run_full_flow(o2)

        execute(o3.id, OrderModel.OPS_REQUIRES_REVIEW, review_reason_code=OrderModel.REVIEW_SKU_UNKNOWN, review_reason_note="SKU desconocido detectado")
        execute(o3.id, OrderModel.OPS_PREPARING)
        execute(o3.id, OrderModel.OPS_READY)
        execute(o3.id, OrderModel.OPS_OUT_FOR_DELIVERY)
        execute(o3.id, OrderModel.OPS_DELIVERED)

        execute(o4.id, OrderModel.OPS_REQUIRES_REVIEW, review_reason_code=OrderModel.REVIEW_CANCEL_AFTER_CONFIRM, review_reason_note="Cliente canceló post-confirm")
        execute(o4.id, OrderModel.OPS_CANCELLED)

        execute(o5.id, OrderModel.OPS_REQUIRES_REVIEW, review_reason_code=OrderModel.REVIEW_MANUAL)

        # Reporte
        from collections import Counter
        for o in orders:
            o.refresh_from_db()
        statuses = [o.ops_status for o in orders]
        cnt = Counter(statuses)
        self.stdout.write(self.style.SUCCESS(f"Conteo por ops_status: {cnt}"))

        for o in orders:
            events = OrderOpsEventModel.objects.filter(order=o).order_by("at")
            self.stdout.write(self.style.WARNING(f"Order {o.id} timeline:"))
            for ev in events:
                self.stdout.write(f" - {ev.at} {ev.from_status} → {ev.to_status} reason={ev.review_reason_code or ''}")
