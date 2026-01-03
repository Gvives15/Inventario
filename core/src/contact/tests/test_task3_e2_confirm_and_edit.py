import json
from django.test import TestCase, Client
from django.core.management import call_command
from inventory.infrastructure.orm.models import Product
from contact.models import OrderModel, ConversationStateModel, Contact
from contact.modules.conversations.domain.conversation_stage import ConversationStage

class Task3E2ConfirmAndEditTests(TestCase):
    def setUp(self):
        for i in range(1, 11):
            Product.objects.create(name=f"Producto {i}", sku=f"DEMO-{i:03d}", category="Bebidas", stock_minimum=0)
        call_command("seed_kiosk_base_list", code="kiosk_base", limit=15)
        self.client = Client()
        self.wh = "wa_t3"
        url = "/api/contacts/webhooks/whatsapp/inbound"
        self.client.post(url, data=json.dumps({"provider":"whatsapp_mock","provider_message_id":"t3_1","whatsapp_id":self.wh,"text":"Hola","raw_payload":{}}), content_type="application/json")
        self.client.post(url, data=json.dumps({"provider":"whatsapp_mock","provider_message_id":"t3_2","whatsapp_id":self.wh,"text":"Nombre: Juan","raw_payload":{}}), content_type="application/json")
        self.client.post(url, data=json.dumps({"provider":"whatsapp_mock","provider_message_id":"t3_3","whatsapp_id":self.wh,"text":"Zona: Norte\nTipo: Kiosco","raw_payload":{}}), content_type="application/json")

    def _post(self, pid, text):
        url = "/api/contacts/webhooks/whatsapp/inbound"
        return self.client.post(url, data=json.dumps({"provider":"whatsapp_mock","provider_message_id":pid,"whatsapp_id":self.wh,"text":text,"raw_payload":{}}), content_type="application/json")

    def test_e2_confirm_sets_status_and_stage(self):
        r = self._post("t3_c1", "OK")
        c = Contact.objects.get(whatsapp_id=self.wh)
        st = ConversationStateModel.objects.get(contact=c)
        o = OrderModel.objects.get(id=st.last_order_id)
        self.assertEqual(o.status, "CONFIRMED")
        self.assertEqual(st.stage, ConversationStage.E4_CONFIRMED.value)

    def test_confirm_is_idempotent(self):
        self._post("t3_c1", "OK")
        c = Contact.objects.get(whatsapp_id=self.wh)
        st1 = ConversationStateModel.objects.get(contact=c)
        oid1 = st1.last_order_id
        r = self._post("t3_c2", "OK")
        st2 = ConversationStateModel.objects.get(contact=c)
        self.assertEqual(st2.last_order_id, oid1)

    def test_e2_edit_add_and_set_qty(self):
        r = self._post("t3_e1", "VER")
        r = self._post("t3_e2", "+ DEMO-001 3")
        self.assertIn("Pedido actualizado", r.json().get("reply",""))
        
        c = Contact.objects.get(whatsapp_id=self.wh)
        st = ConversationStateModel.objects.get(contact=c)
        self.assertEqual(st.stage, ConversationStage.E3_ADJUSTMENTS.value)

        r = self._post("t3_e3", "= DEMO-001 5")
        self.assertIn("Pedido actualizado", r.json().get("reply",""))
        
    def test_e2_patch_moves_to_e3(self):
        c = Contact.objects.get(whatsapp_id=self.wh)
        st = ConversationStateModel.objects.get(contact=c)
        self.assertEqual(st.stage, ConversationStage.E2_PROPOSAL.value)
        
        self._post("t3_e_patch", "+ DEMO-001 3")
        
        st.refresh_from_db()
        self.assertEqual(st.stage, ConversationStage.E3_ADJUSTMENTS.value)

    def test_edit_after_confirm_rejected(self):
        self._post("t3_c1", "OK")
        r = self._post("t3_e2", "+ DEMO-003 2")
        self.assertIn("Pedido confirmado", r.json().get("reply",""))
