import json
from django.test import TestCase, Client
from django.core.management import call_command
from inventory.infrastructure.orm.models import Product

class E2EKioskProposalCleanTests(TestCase):
    def setUp(self):
        for i in range(1, 11):
            Product.objects.create(name=f"Producto {i}", sku=f"DEMO-{i:03d}", category="Bebidas", stock_minimum=0)
        call_command("seed_kiosk_base_list", code="kiosk_base", limit=15)

    def test_proposal_has_valid_items(self):
        client = Client()
        wh = "5491199999999"
        url = "/api/contacts/webhooks/whatsapp/inbound"
        payload1 = {"provider":"whatsapp_mock","provider_message_id":"e2e_t_clean_1","whatsapp_id":wh,"text":"Hola","raw_payload":{}}
        payload3 = {"provider":"whatsapp_mock","provider_message_id":"e2e_t_clean_2","whatsapp_id":wh,"text":"Nombre: Pedro","raw_payload":{}}
        payload4 = {"provider":"whatsapp_mock","provider_message_id":"e2e_t_clean_3","whatsapp_id":wh,"text":"Zona: Norte\nTipo: Kiosco","raw_payload":{}}
        client.post(url, data=json.dumps(payload1), content_type="application/json")
        client.post(url, data=json.dumps(payload3), content_type="application/json")
        r = client.post(url, data=json.dumps(payload4), content_type="application/json")
        reply = r.json().get("reply","")
        self.assertIn("Propuesta #", reply)
        self.assertNotIn("(SKU:1)", reply)
        self.assertNotIn(" 2x m", reply)
