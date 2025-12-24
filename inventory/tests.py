from django.test import TestCase
from django.contrib.auth.models import User
from inventory.src.infrastructure.orm.models import Product, StockMovement
import json

class StockRuleTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u", password="p")
        resp = self.client.post("/api/auth/token", data=json.dumps({"username": "u", "password": "p"}), content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        self.token = resp.json()["access_token"]
        self.auth = {"HTTP_AUTHORIZATION": f"Bearer {self.token}"}

    def _create_product(self):
        resp = self.client.post(
            "/api/inventory/products",
            data=json.dumps({"name": "A", "sku": "SKU1", "category": "cat", "stock_minimum": 1}),
            content_type="application/json",
            **self.auth,
        )
        self.assertEqual(resp.status_code, 200)
        return resp.json()["id"]

    def test_patch_product_rejects_unknown_field_stock_current(self):
        pid = self._create_product()
        resp2 = self.client.patch(
            f"/api/inventory/products/{pid}",
            data=json.dumps({"stock_current": 10}),
            content_type="application/json",
            **self.auth,
        )
        self.assertEqual(resp2.status_code, 422)

    def test_adjust_requires_reason(self):
        pid = self._create_product()
        r = self.client.post(
            "/api/inventory/stock/adjust-to-count",
            data=json.dumps({"product_id": pid, "counted_stock": 10, "reason": ""}),
            content_type="application/json",
            **self.auth,
        )
        self.assertEqual(r.status_code, 400)

    def test_exit_cannot_go_negative(self):
        pid = self._create_product()
        r = self.client.post(
            "/api/inventory/stock/exit",
            data=json.dumps({"product_id": pid, "quantity": 1, "reason": "Venta"}),
            content_type="application/json",
            **self.auth,
        )
        self.assertEqual(r.status_code, 400)

    def test_adjust_to_count_updates_stock_and_creates_movement(self):
        pid = self._create_product()
        r = self.client.post(
            "/api/inventory/stock/adjust-to-count",
            data=json.dumps({"product_id": pid, "counted_stock": 5, "reason": "Stock inicial"}),
            content_type="application/json",
            **self.auth,
        )
        self.assertEqual(r.status_code, 200)
        p = Product.objects.get(id=pid)
        self.assertEqual(p.stock_current, 5)
        mv = StockMovement.objects.filter(product_id=pid).order_by("-id").first()
        self.assertIsNotNone(mv)
        self.assertEqual(mv.resulting_stock, 5)

    def test_jwt_sets_request_user_and_created_by_not_null(self):
        pid = self._create_product()
        r = self.client.post(
            "/api/inventory/stock/entry",
            data=json.dumps({"product_id": pid, "quantity": 2, "reason": "Compra"}),
            content_type="application/json",
            **self.auth,
        )
        self.assertEqual(r.status_code, 200)
        mv = StockMovement.objects.filter(product_id=pid).order_by("-id").first()
        self.assertIsNotNone(mv)
        self.assertIsNotNone(mv.created_by)
        self.assertEqual(mv.created_by_id, self.user.id)

    def test_entry_requires_reason(self):
        pid = self._create_product()
        r = self.client.post(
            "/api/inventory/stock/entry",
            data=json.dumps({"product_id": pid, "quantity": 2, "reason": ""}),
            content_type="application/json",
            **self.auth,
        )
        self.assertEqual(r.status_code, 400)

    def test_exit_requires_reason(self):
        pid = self._create_product()
        r = self.client.post(
            "/api/inventory/stock/exit",
            data=json.dumps({"product_id": pid, "quantity": 1, "reason": ""}),
            content_type="application/json",
            **self.auth,
        )
        self.assertEqual(r.status_code, 400)

    def test_movement_type_choices_enforced_in_repo(self):
        p = Product.objects.create(name="A", sku="SKUX", category="", stock_minimum=0)
        from inventory.src.infrastructure.orm.stock_movement_repo import create as create_mv
        with self.assertRaises(ValueError):
            create_mv(p, 1, "bad", "test", 1, user=self.user)
