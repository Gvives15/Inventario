from django.test import TestCase
from django.core.exceptions import ValidationError
from contact.models import Contact, OrderModel, OrderOpsEventModel
from contact.modules.orders.domain.order_status import OrderStatus
from contact.modules.orders.application.commands.change_ops_status_cmd import execute


class ReviewResolutionTests(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(name="Cliente", type=Contact.TYPE_CLIENT)
        self.order = OrderModel.objects.create(contact=self.contact, status=OrderStatus.CONFIRMED.value)

    def test_resolve_review_requires_note(self):
        execute(self.order.id, OrderModel.OPS_REQUIRES_REVIEW, review_reason_code=OrderModel.REVIEW_MANUAL)
        with self.assertRaises(ValidationError):
            execute(self.order.id, OrderModel.OPS_PREPARING, resolve_review=True)

    def test_resolve_review_to_preparing_creates_ops_event(self):
        execute(self.order.id, OrderModel.OPS_REQUIRES_REVIEW, review_reason_code=OrderModel.REVIEW_MANUAL)
        order = execute(self.order.id, OrderModel.OPS_PREPARING, note="RESOLVED: ok", resolve_review=True)
        self.assertEqual(order.ops_status, OrderModel.OPS_PREPARING)
        self.assertTrue(OrderOpsEventModel.objects.filter(order=order, to_status=OrderModel.OPS_PREPARING).exists())

    def test_resolve_review_to_cancelled_creates_ops_event(self):
        execute(self.order.id, OrderModel.OPS_REQUIRES_REVIEW, review_reason_code=OrderModel.REVIEW_MANUAL)
        order = execute(self.order.id, OrderModel.OPS_CANCELLED, note="RESOLVED: cancel", resolve_review=True)
        self.assertEqual(order.ops_status, OrderModel.OPS_CANCELLED)
        self.assertTrue(OrderOpsEventModel.objects.filter(order=order, to_status=OrderModel.OPS_CANCELLED).exists())

    def test_resolve_review_fails_if_not_in_review(self):
        with self.assertRaises(ValidationError):
            execute(self.order.id, OrderModel.OPS_PREPARING, note="RESOLVED: attempt", resolve_review=True)
