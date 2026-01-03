from django.core.management import call_command
from django.test import TestCase
from inventory.infrastructure.orm.models import Product, ProductListModel, ProductListItemModel

class SeedKioskBaseFiltersInvalidTests(TestCase):
    def test_seed_excludes_invalid_and_includes_valids(self):
        Product.objects.create(name="m", sku="1", category="", stock_minimum=0)
        for i in range(1, 11):
            Product.objects.create(name=f"Producto {i}", sku=f"DEMO-{i:03d}", category="Bebidas", stock_minimum=0)
        call_command("cleanup_catalog_products", "--apply", "--deactivate-invalid")
        call_command("seed_kiosk_base_list", code="kiosk_base", limit=15)
        plist = ProductListModel.objects.get(code="kiosk_base")
        items = ProductListItemModel.objects.filter(product_list=plist).select_related("product")
        self.assertGreaterEqual(items.count(), 10)
        skus = [it.product.sku for it in items]
        self.assertNotIn("1", skus)
