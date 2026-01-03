from django.test import TestCase
from contact.modules.conversations.infrastructure.orm.contact_repo import upsert_minimal
from contact.modules.orders.application.commands.create_order_proposal_cmd import execute as create_proposal
from contact.models import OrderModel
from inventory.infrastructure.orm.models import Product, ProductListModel, ProductListItemModel

class TemplateFromInventoryTests(TestCase):
    def setUp(self):
        upsert_minimal("wa1", "Juan", "Norte", "Kiosco")

    def test_missing_list_uses_fallback_items(self):
        order_id = create_proposal("wa1")
        order = OrderModel.objects.prefetch_related("items").get(id=order_id)
        self.assertEqual(order.status, "PROPOSED")
        self.assertTrue(10 <= order.items.count() <= 15)

    def test_existing_list_creates_order_with_real_skus(self):
        p1 = Product.objects.create(name="P1", sku="SKU1", category="", stock_minimum=0)
        plist = ProductListModel.objects.create(code="kiosk_base", name="kiosk_base", is_active=True)
        ProductListItemModel.objects.create(product_list=plist, product=p1, default_qty=2, sort_order=1)
        order_id = create_proposal("wa1")
        order = OrderModel.objects.prefetch_related("items").get(id=order_id)
        self.assertEqual(order.status, "PROPOSED")
        self.assertTrue(order.items.count() >= 1)
        self.assertTrue(order.items.filter(product_ref="SKU:SKU1").exists())
