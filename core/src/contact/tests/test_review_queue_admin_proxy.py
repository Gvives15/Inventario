from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from contact.models import Contact, OrderModel, OrderReviewQueue
from contact.admin import ReviewQueueAdmin

class ReviewQueueAdminProxyTests(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(name="Cliente A", type=Contact.TYPE_CLIENT)
        
        # Order in REVIEW
        self.order_review = OrderModel.objects.create(
            contact=self.contact, 
            status="CONFIRMED", 
            ops_status=OrderModel.OPS_REQUIRES_REVIEW
        )
        
        # Order in PREPARING (should not be in review queue)
        self.order_preparing = OrderModel.objects.create(
            contact=self.contact, 
            status="CONFIRMED", 
            ops_status=OrderModel.OPS_PREPARING
        )
        
        self.site = AdminSite()
        self.ma = ReviewQueueAdmin(OrderReviewQueue, self.site)

    def test_review_queue_admin_queryset_returns_only_review_orders(self):
        qs = self.ma.get_queryset(None)
        ids = set(qs.values_list("id", flat=True))
        
        self.assertIn(self.order_review.id, ids)
        self.assertNotIn(self.order_preparing.id, ids)
