from django.test import TestCase
from inventory.infrastructure.orm.models import Product, ProductListModel, ProductListItemModel
from inventory.application.queries.get_product_list_q import execute
from inventory.domain.errors import ProductListNotFound, ProductListInactive, ProductListEmpty

class GetProductListQTests(TestCase):
    def test_list_not_exists_raises(self):
        with self.assertRaises(ProductListNotFound):
            execute("missing")

    def test_list_exists_inactive_raises(self):
        ProductListModel.objects.create(code="kiosk_base", name="kiosk_base", is_active=False)
        with self.assertRaises(ProductListInactive):
            execute("kiosk_base")

    def test_list_exists_empty_raises(self):
        ProductListModel.objects.create(code="kiosk_base", name="kiosk_base", is_active=True)
        with self.assertRaises(ProductListEmpty):
            execute("kiosk_base")

    def test_list_with_items_returns_dict(self):
        p1 = Product.objects.create(name="P1", sku="SKU1", category="", stock_minimum=0)
        plist = ProductListModel.objects.create(code="kiosk_base", name="kiosk_base", is_active=True)
        ProductListItemModel.objects.create(product_list=plist, product=p1, default_qty=2, sort_order=1)
        out = execute("kiosk_base")
        self.assertEqual(out["code"], "kiosk_base")
        self.assertTrue(len(out["items"]) >= 1)
        item = out["items"][0]
        self.assertEqual(item["sku"], "SKU1")
        self.assertEqual(item["name"], "P1")
        self.assertEqual(item["default_qty"], 2)
