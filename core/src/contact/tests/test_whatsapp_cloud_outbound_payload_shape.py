import json
from django.test import TestCase
from contact.modules.gateways.whatsapp_cloud.infrastructure.wa_client import build_text_payload, build_product_list_payload

class WhatsAppOutboundPayloadTests(TestCase):
    def test_send_text_payload_shape(self):
        p = build_text_payload("5491199999999", "Hola")
        self.assertEqual(p["messaging_product"], "whatsapp")
        self.assertEqual(p["to"], "5491199999999")
        self.assertEqual(p["type"], "text")
        self.assertEqual(p["text"]["body"], "Hola")

    def test_send_product_list_payload_shape(self):
        skus = ["DEMO-001", "DEMO-002", "DEMO-003"]
        p = build_product_list_payload("5491199999999", "CATALOG_ID_HERE", skus)
        self.assertEqual(p["messaging_product"], "whatsapp")
        self.assertEqual(p["to"], "5491199999999")
        self.assertEqual(p["type"], "interactive")
        self.assertEqual(p["interactive"]["type"], "product_list")
        self.assertEqual(p["interactive"]["action"]["catalog_id"], "CATALOG_ID_HERE")
        items = p["interactive"]["action"]["sections"][0]["product_items"]
        self.assertEqual([i["product_retailer_id"] for i in items], skus)

