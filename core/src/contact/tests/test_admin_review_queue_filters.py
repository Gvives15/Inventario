from django.test import TestCase
from django.utils import timezone
from contact.models import Contact, OrderModel
from contact.admin import ReviewQueueFilter
from django.contrib.admin.sites import AdminSite
from django.contrib import admin


class DummyModelAdmin(admin.ModelAdmin):
    pass


class AdminReviewQueueFilterTests(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(name="Cliente", type=Contact.TYPE_CLIENT)
        self.order_a = OrderModel.objects.create(contact=self.contact, status="CONFIRMED", ops_status=OrderModel.OPS_REQUIRES_REVIEW)
        self.order_b = OrderModel.objects.create(contact=self.contact, status="CONFIRMED", ops_status=OrderModel.OPS_REQUIRES_REVIEW)
        self.order_c = OrderModel.objects.create(contact=self.contact, status="CONFIRMED", ops_status=OrderModel.OPS_CONFIRMED)
        self.site = AdminSite()
        self.ma = DummyModelAdmin(OrderModel, self.site)

    def _filter(self, val):
        rf = ReviewQueueFilter(self.site, {}, OrderModel, self.ma)
        rf.used_parameters = {}
        rf.value = lambda: val
        return rf

    def test_review_filter_pending_returns_only_review_orders(self):
        rf = self._filter("pending")
        qs = rf.queryset(None, OrderModel.objects.all())
        ids = set(qs.values_list("id", flat=True))
        self.assertIn(self.order_a.id, ids)
        self.assertIn(self.order_b.id, ids)
        self.assertNotIn(self.order_c.id, ids)

    def test_review_filter_overdue_returns_only_deadline_past(self):
        self.order_a.review_deadline_at = timezone.now() - timezone.timedelta(hours=1)
        self.order_a.save(update_fields=["review_deadline_at", "updated_at"])
        self.order_b.review_deadline_at = timezone.now() + timezone.timedelta(hours=1)
        self.order_b.save(update_fields=["review_deadline_at", "updated_at"])
        rf = self._filter("overdue")
        qs = rf.queryset(None, OrderModel.objects.all())
        ids = set(qs.values_list("id", flat=True))
        self.assertIn(self.order_a.id, ids)
        self.assertNotIn(self.order_b.id, ids)

    def test_review_filter_no_deadline_returns_only_review_without_deadline(self):
        self.order_a.review_deadline_at = None
        self.order_a.save(update_fields=["review_deadline_at", "updated_at"])
        self.order_b.review_deadline_at = timezone.now() + timezone.timedelta(hours=1)
        self.order_b.save(update_fields=["review_deadline_at", "updated_at"])
        rf = self._filter("no_deadline")
        qs = rf.queryset(None, OrderModel.objects.all())
        ids = set(qs.values_list("id", flat=True))
        self.assertIn(self.order_a.id, ids)
        self.assertNotIn(self.order_b.id, ids)
