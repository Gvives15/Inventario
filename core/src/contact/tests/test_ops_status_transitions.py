from django.test import TestCase
from django.core.exceptions import ValidationError
from contact.models import Contact, OrderModel, OrderOpsEventModel
from contact.modules.orders.application.commands.change_ops_status_cmd import execute
from contact.modules.orders.domain.order_status import OrderStatus

class OpsStatusTransitionTests(TestCase):
    def setUp(self):
        self.c = Contact.objects.create(whatsapp_id="wa1", name="P", business_type="B", type=Contact.TYPE_CLIENT)
        self.o = OrderModel.objects.create(contact=self.c, status=OrderStatus.CONFIRMED.value)

    def test_blocks_paid_without_delivered(self):
        with self.assertRaises(ValidationError):
            execute(self.o.id, OrderModel.OPS_PAID)

    def test_blocks_review_without_reason_code(self):
        with self.assertRaises(ValidationError):
            execute(self.o.id, OrderModel.OPS_REQUIRES_REVIEW)

    def test_blocks_ops_if_order_not_confirmed_except_cancel(self):
        o2 = OrderModel.objects.create(contact=self.c, status=OrderStatus.PROPOSED.value)
        execute(o2.id, OrderModel.OPS_CANCELLED)  # allowed
        with self.assertRaises(ValidationError):
            execute(o2.id, OrderModel.OPS_PREPARING)

    def test_valid_transition_creates_ops_event(self):
        execute(self.o.id, OrderModel.OPS_PREPARING)
        execute(self.o.id, OrderModel.OPS_READY)
        execute(self.o.id, OrderModel.OPS_OUT_FOR_DELIVERY)
        execute(self.o.id, OrderModel.OPS_DELIVERED)
        execute(self.o.id, OrderModel.OPS_PAID)
        events = OrderOpsEventModel.objects.filter(order_id=self.o.id).order_by("at")
        self.assertGreaterEqual(events.count(), 5)
        last = events.last()
        self.assertEqual(last.to_status, OrderModel.OPS_PAID)
