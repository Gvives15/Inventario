import json
import hmac
import hashlib
from django.test import TestCase, Client
from django.test.utils import override_settings
from inventory.infrastructure.orm.models import Product
from contact.models import OrderModel

ORDER_PAYLOAD_ALL_KNOWN = {
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "WABA_ID",
      "changes": [
        {
          "field": "messages",
          "value": {
            "messaging_product": "whatsapp",
            "metadata": { "phone_number_id": "PHONE_NUMBER_ID" },
            "contacts": [{ "wa_id": "5491199999999", "profile": { "name": "Pedro" } }],
            "messages": [
              {
                "from": "5491199999999",
                "id": "wamid.ORDERMSGID123",
                "timestamp": "1767415200",
                "type": "order",
                "order": {
                  "catalog_id": "CATALOG_ID_HERE",
                  "text": "Nota opcional del cliente",
                  "product_items": [
                    { "product_retailer_id": "DEMO-001", "quantity": 2, "item_price": "100.00", "currency": "ARS" },
                    { "product_retailer_id": "DEMO-002", "quantity": 1, "item_price": "250.00", "currency": "ARS" }
                  ]
                }
              }
            ]
          }
        }
      ]
    }
  ]
}

ORDER_PAYLOAD_WITH_UNKNOWN = {
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "WABA_ID",
      "changes": [
        {
          "field": "messages",
          "value": {
            "messaging_product": "whatsapp",
            "metadata": { "phone_number_id": "PHONE_NUMBER_ID" },
            "contacts": [{ "wa_id": "5491199999999", "profile": { "name": "Pedro" } }],
            "messages": [
              {
                "from": "5491199999999",
                "id": "wamid.ORDERMSGID456",
                "timestamp": "1767415200",
                "type": "order",
                "order": {
                  "catalog_id": "CATALOG_ID_HERE",
                  "text": "Nota opcional del cliente",
                  "product_items": [
                    { "product_retailer_id": "DEMO-001", "quantity": 2, "item_price": "100.00", "currency": "ARS" },
                    { "product_retailer_id": "UNKNOWN-777", "quantity": 1, "item_price": "250.00", "currency": "ARS" }
                  ]
                }
              }
            ]
          }
        }
      ]
    }
  ]
}

class WhatsAppOrderHandlerTests(TestCase):
    @override_settings(WHATSAPP_APP_SECRET="ordersecret")
    def test_order_webhook_creates_confirmed_when_all_skus_known(self):
        Product.objects.create(name="A", sku="DEMO-001")
        Product.objects.create(name="B", sku="DEMO-002")
        client = Client()
        raw = json.dumps(ORDER_PAYLOAD_ALL_KNOWN).encode("utf-8")
        sig = hmac.new(b"ordersecret", raw, hashlib.sha256).hexdigest()
        headers = {"HTTP_X_HUB_SIGNATURE_256": f"sha256={sig}"}
        r = client.post("/api/contacts/webhooks/whatsapp_cloud/", data=raw, content_type="application/json", **headers)
        self.assertEqual(r.status_code, 200)
        o = OrderModel.objects.latest("id")
        self.assertEqual(o.status, "CONFIRMED")
        self.assertEqual(o.items.count(), 2)

    @override_settings(WHATSAPP_APP_SECRET="ordersecret")
    def test_order_webhook_sets_requires_review_when_any_unknown_sku(self):
        Product.objects.create(name="A", sku="DEMO-001")
        client = Client()
        raw = json.dumps(ORDER_PAYLOAD_WITH_UNKNOWN).encode("utf-8")
        sig = hmac.new(b"ordersecret", raw, hashlib.sha256).hexdigest()
        headers = {"HTTP_X_HUB_SIGNATURE_256": f"sha256={sig}"}
        r = client.post("/api/contacts/webhooks/whatsapp_cloud/", data=raw, content_type="application/json", **headers)
        self.assertEqual(r.status_code, 200)
        o = OrderModel.objects.latest("id")
        self.assertEqual(o.status, "REQUIRES_REVIEW")
        self.assertEqual(o.items.count(), 2)

