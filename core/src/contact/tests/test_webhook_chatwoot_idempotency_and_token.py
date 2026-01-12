import json
from django.test import TestCase, Client
from django.conf import settings
from django.test.utils import override_settings


class ChatwootWebhookTests(TestCase):
    @override_settings()
    def test_rejects_without_token(self):
        client = Client()
        url = "/api/contacts/webhooks/chatwoot/"
        payload = {"event": "message_created", "message": {"id": 1, "content": "Hola", "message_type": "incoming"}, "conversation": {"id": 10, "contact": {"id": 100}}}
        r = client.post(url, data=json.dumps(payload), content_type="application/json")
        self.assertEqual(r.status_code, 401)

    @override_settings(CHATWOOT_WEBHOOK_TOKEN="secret")
    def test_processes_once_idempotent(self):
        client = Client()
        url = "/api/contacts/webhooks/chatwoot/"
        payload = {"event": "message_created", "message": {"id": 2, "content": "Hola", "message_type": "incoming"}, "conversation": {"id": 20, "contact": {"id": 200}}}
        headers = {"HTTP_X_O11CE_WEBHOOK_TOKEN": "secret"}
        r1 = client.post(url, data=json.dumps(payload), content_type="application/json", **headers)
        self.assertEqual(r1.status_code, 200)
        r2 = client.post(url, data=json.dumps(payload), content_type="application/json", **headers)
        self.assertEqual(r2.status_code, 200)
