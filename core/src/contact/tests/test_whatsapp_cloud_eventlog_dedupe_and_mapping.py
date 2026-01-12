import json
import hmac
import hashlib
from django.test import TestCase, Client
from django.test.utils import override_settings
from contact.modules.messaging.infrastructure.orm.message_event_models import MessageEventLogModel

class WhatsAppCloudEventLogTests(TestCase):
    @override_settings(WHATSAPP_APP_SECRET="s3cret")
    def test_dedupe_message_processed_once(self):
        client = Client()
        payload = {"entry": [{"changes": [{"value": {}}]}]}
        payload["entry"][0]["changes"][0]["value"]["messages"] = [{"id": "m100", "text": {"body": "Hola"}}]
        payload["entry"][0]["changes"][0]["value"]["contacts"] = [{"wa_id": "54911"}]
        raw = json.dumps(payload).encode("utf-8")
        sig = hmac.new(b"s3cret", raw, hashlib.sha256).hexdigest()
        headers = {"HTTP_X_HUB_SIGNATURE_256": f"sha256={sig}"}
        r1 = client.post("/api/contacts/webhooks/whatsapp_cloud/", data=raw, content_type="application/json", **headers)
        self.assertEqual(r1.status_code, 200)
        r2 = client.post("/api/contacts/webhooks/whatsapp_cloud/", data=raw, content_type="application/json", **headers)
        self.assertEqual(r2.status_code, 200)
        obj = MessageEventLogModel.objects.get(provider="whatsapp_cloud", external_event_id="wa:in:m100")
        self.assertEqual(obj.status, "PROCESSED")
        self.assertEqual(obj.direction, "IN")
        self.assertEqual(obj.conversation_external_id, "54911")

    def test_mapping_text(self):
        from contact.modules.gateways.whatsapp_cloud.domain.mapping import to_inbound_envelope
        payload = {"entry": [{"changes": [{"value": {}}]}]}
        payload["entry"][0]["changes"][0]["value"]["messages"] = [{"id": "m9", "text": {"body": "Hi"}}]
        payload["entry"][0]["changes"][0]["value"]["contacts"] = [{"wa_id": "123"}]
        env = to_inbound_envelope(payload)
        self.assertEqual(env["provider"], "whatsapp_cloud")
        self.assertEqual(env["external_event_id"], "m9")
        self.assertEqual(env["contact_external_id"], "123")
        self.assertEqual(env["thread_key"], "123")
        self.assertEqual(env["message_type"], "text")
        self.assertEqual(env["content"], "Hi")

    @override_settings(WHATSAPP_APP_SECRET="s3cret")
    def test_webhook_processes_multiple_messages(self):
        # DoD A: Batch processing
        client = Client()
        payload = {"entry": [{"changes": [{"value": {}}]}]}
        payload["entry"][0]["changes"][0]["value"]["messages"] = [
            {"id": "msg_batch_1", "text": {"body": "First"}},
            {"id": "msg_batch_2", "text": {"body": "Second"}}
        ]
        payload["entry"][0]["changes"][0]["value"]["contacts"] = [{"wa_id": "54911"}]
        
        raw = json.dumps(payload).encode("utf-8")
        sig = hmac.new(b"s3cret", raw, hashlib.sha256).hexdigest()
        headers = {"HTTP_X_HUB_SIGNATURE_256": f"sha256={sig}"}
        
        resp = client.post("/api/contacts/webhooks/whatsapp_cloud/", data=raw, content_type="application/json", **headers)
        self.assertEqual(resp.status_code, 200)
        
        # Verify both are processed
        m1 = MessageEventLogModel.objects.filter(external_event_id="wa:in:msg_batch_1").first()
        m2 = MessageEventLogModel.objects.filter(external_event_id="wa:in:msg_batch_2").first()
        self.assertIsNotNone(m1)
        self.assertIsNotNone(m2)
        self.assertEqual(m1.status, "PROCESSED")
        self.assertEqual(m2.status, "PROCESSED")

    @override_settings(WHATSAPP_APP_SECRET="s3cret")
    def test_duplicate_does_not_overwrite_processed(self):
        # DoD B: EventLog correcto
        client = Client()
        # 1. Simulate existing PROCESSED event
        MessageEventLogModel.objects.create(
            provider="whatsapp_cloud",
            external_event_id="wa:in:msg_dup_test",
            direction="IN",
            status="PROCESSED",
            payload_json={}
        )
        
        # 2. Receive same message via webhook
        payload = {"entry": [{"changes": [{"value": {}}]}]}
        payload["entry"][0]["changes"][0]["value"]["messages"] = [{"id": "msg_dup_test", "text": {"body": "Dup"}}]
        payload["entry"][0]["changes"][0]["value"]["contacts"] = [{"wa_id": "54911"}]
        
        raw = json.dumps(payload).encode("utf-8")
        sig = hmac.new(b"s3cret", raw, hashlib.sha256).hexdigest()
        headers = {"HTTP_X_HUB_SIGNATURE_256": f"sha256={sig}"}
        
        resp = client.post("/api/contacts/webhooks/whatsapp_cloud/", data=raw, content_type="application/json", **headers)
        self.assertEqual(resp.status_code, 200)
        
        # 3. Verify original is still PROCESSED
        original = MessageEventLogModel.objects.get(external_event_id="wa:in:msg_dup_test")
        self.assertEqual(original.status, "PROCESSED")
        
        # 4. Verify duplicate log exists (SKIPPED_DUPLICATE)
        dup = MessageEventLogModel.objects.filter(external_event_id="dup:wa:in:msg_dup_test").first()
        self.assertIsNotNone(dup)
        self.assertEqual(dup.status, "SKIPPED_DUPLICATE")
