import json
import hmac
import hashlib
from django.test import TestCase, Client
from django.test.utils import override_settings

class WhatsAppCloudWebhookTests(TestCase):
    @override_settings(WHATSAPP_VERIFY_TOKEN="verify123")
    def test_get_verify_ok(self):
        client = Client()
        url = "/api/contacts/webhooks/whatsapp_cloud/?hub.mode=subscribe&hub.verify_token=verify123&hub.challenge=abc"
        r = client.get(url)
        self.assertEqual(r.status_code, 200)
        body = json.loads(r.content.decode())
        self.assertEqual(body.get("hub.challenge"), "abc")

    @override_settings(WHATSAPP_VERIFY_TOKEN="verify123")
    def test_get_verify_unauthorized(self):
        client = Client()
        url = "/api/contacts/webhooks/whatsapp_cloud/?hub.mode=subscribe&hub.verify_token=wrong&hub.challenge=abc"
        r = client.get(url)
        self.assertEqual(r.status_code, 401)

    @override_settings(WHATSAPP_APP_SECRET="appsecret123")
    def test_post_signature_ok(self):
        client = Client()
        payload = {"entry": [{"changes": [{"value": {}}]}]}
        payload["entry"][0]["changes"][0]["value"]["messages"] = [{"id": "m1"}]
        payload["entry"][0]["changes"][0]["value"]["contacts"] = [{"wa_id": "54911"}]
        raw = json.dumps(payload).encode("utf-8")
        sig = hmac.new(b"appsecret123", raw, hashlib.sha256).hexdigest()
        headers = {"HTTP_X_HUB_SIGNATURE_256": f"sha256={sig}"}
        r = client.post("/api/contacts/webhooks/whatsapp_cloud/", data=raw, content_type="application/json", **headers)
        self.assertEqual(r.status_code, 200)

    @override_settings(WHATSAPP_APP_SECRET="appsecret123")
    def test_post_signature_invalid(self):
        client = Client()
        payload = {"entry": [{"changes": [{"value": {}}]}]}
        payload["entry"][0]["changes"][0]["value"]["messages"] = [{"id": "m2"}]
        payload["entry"][0]["changes"][0]["value"]["contacts"] = [{"wa_id": "54911"}]
        raw = json.dumps(payload).encode("utf-8")
        headers = {"HTTP_X_HUB_SIGNATURE_256": "sha256=invalid"}
        r = client.post("/api/contacts/webhooks/whatsapp_cloud/", data=raw, content_type="application/json", **headers)
        self.assertEqual(r.status_code, 401)
