from django.test import TestCase, Client
from contact.models import MessageInboundModel, Contact, ConversationStateModel, OrderModel


client = Client()


class WhatsAppInboundTests(TestCase):
    def setUp(self):
        self.url = "/api/contacts/webhooks/whatsapp/inbound"

    def _post(self, payload: dict):
        return client.post(self.url, data=payload, content_type="application/json")

    def test_dedupe_by_provider_message_id(self):
        payload = {
            "provider": "whatsapp_mock",
            "provider_message_id": "abc123",
            "whatsapp_id": "w1",
            "text": "hola",
            "raw_payload": {},
        }
        r1 = self._post(payload)
        self.assertEqual(r1.status_code, 200)
        self.assertEqual(MessageInboundModel.objects.count(), 1)
        r2 = self._post(payload)
        self.assertEqual(r2.status_code, 200)
        self.assertEqual(MessageInboundModel.objects.count(), 1)

    def test_new_contact_prompts_for_e1(self):
        payload = {
            "provider": "whatsapp_mock",
            "provider_message_id": "m1",
            "whatsapp_id": "w2",
            "text": "hola",
            "raw_payload": {},
        }
        r = self._post(payload)
        self.assertEqual(r.status_code, 200)
        self.assertIn("Nombre:", r.json()["reply"])
        c = Contact.objects.get(whatsapp_id="w2")
        self.assertTrue(ConversationStateModel.objects.filter(contact_id=c.id).exists())

    def test_e1_complete_triggers_proposal(self):
        payload = {
            "provider": "whatsapp_mock",
            "provider_message_id": "m2",
            "whatsapp_id": "w3",
            "text": "Nombre: Ana\nZona: CABA\nTipo: Kiosco",
            "raw_payload": {},
        }
        r = self._post(payload)
        self.assertEqual(r.status_code, 200)
        self.assertIn("Propuesta #", r.json()["reply"]) 
        c = Contact.objects.get(whatsapp_id="w3")
        state = ConversationStateModel.objects.get(contact_id=c.id)
        self.assertEqual(state.stage, "E2_PROPOSAL")
        self.assertIsNotNone(state.last_order)

    def test_reuses_existing_proposed_order(self):
        payload = {
            "provider": "whatsapp_mock",
            "provider_message_id": "m3",
            "whatsapp_id": "w4",
            "text": "Nombre: Ana\nZona: CABA\nTipo: Kiosco",
            "raw_payload": {},
        }
        r1 = self._post(payload)
        self.assertEqual(r1.status_code, 200)
        c = Contact.objects.get(whatsapp_id="w4")
        state = ConversationStateModel.objects.get(contact_id=c.id)
        o1 = state.last_order
        # enviar otro mensaje con distinto provider_message_id (no duplicado de inbound)
        payload["provider_message_id"] = "m4"
        r2 = self._post(payload)
        self.assertEqual(r2.status_code, 200)
        state = ConversationStateModel.objects.get(contact_id=c.id)
        self.assertEqual(state.last_order_id, o1.id)

    def test_e2_stage_neutral_text_returns_proposal(self):
        # 1. Crear contacto con E1 completo
        payload = {
            "provider": "whatsapp_mock",
            "provider_message_id": "m5",
            "whatsapp_id": "w5",
            "text": "Nombre: Juan\nZona: Sur\nTipo: Almacen",
            "raw_payload": {},
        }
        r1 = self._post(payload)
        self.assertIn("Propuesta #", r1.json()["reply"])
        
        # 2. Enviar mensaje neutro "Gracias"
        payload_neutral = {
            "provider": "whatsapp_mock",
            "provider_message_id": "m6",
            "whatsapp_id": "w5",
            "text": "Gracias",
            "raw_payload": {},
        }
        r2 = self._post(payload_neutral)
        
        # 3. Debe devolver Propuesta, NO prompt E1
        self.assertIn("Propuesta #", r2.json()["reply"])
        self.assertNotIn("Nombre:", r2.json()["reply"])
        
        # 4. Verificar que NO creó una orden nueva
        c = Contact.objects.get(whatsapp_id="w5")
        orders_count = OrderModel.objects.filter(contact_id=c.id).count()
        self.assertEqual(orders_count, 1)
