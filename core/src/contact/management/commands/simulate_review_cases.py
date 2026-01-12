from django.core.management.base import BaseCommand
from django.utils import timezone
from contact.models import Contact, OrderModel
from contact.modules.orders.domain.order_status import OrderStatus
from contact.modules.orders.application.commands.change_ops_status_cmd import execute

class Command(BaseCommand):
    help = "Crea 8 órdenes CONFIRMED y las pone en REQUIRES_REVIEW con códigos y notas"

    def handle(self, *args, **options):
        contact, _ = Contact.objects.get_or_create(name="Demo Cliente", type=Contact.TYPE_CLIENT)
        codes = [
            OrderModel.REVIEW_SKU_UNKNOWN,
            OrderModel.REVIEW_CANCEL_AFTER_CONFIRM,
            OrderModel.REVIEW_CHANGE_AFTER_CONFIRM,
            OrderModel.REVIEW_ORDER_REPLACED,
            OrderModel.REVIEW_ADDRESS_OUT_OF_ZONE,
            OrderModel.REVIEW_CUSTOMER_NOT_AVAILABLE,
            OrderModel.REVIEW_PAYMENT_ISSUE,
            OrderModel.REVIEW_MANUAL,
        ]
        created = 0
        for code in codes:
            order = OrderModel.objects.create(contact=contact, status=OrderStatus.CONFIRMED.value)
            note = f"qué pasó: caso {code}\nacción sugerida: revisar y actuar\ndeadline: {timezone.now().date().isoformat()}"
            execute(order.id, OrderModel.OPS_REQUIRES_REVIEW, review_reason_code=code, review_reason_note=note)
            created += 1
        self.stdout.write(self.style.SUCCESS(f"{created} órdenes en REQUIRES_REVIEW"))
