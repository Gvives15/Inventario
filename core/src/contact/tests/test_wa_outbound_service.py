from django.test import TestCase
from unittest.mock import patch
from contact.modules.gateways.whatsapp_cloud.application.services.wa_outbound_service import send_safe_text, send_safe_product_list
from contact.modules.messaging.infrastructure.orm.message_event_models import MessageEventLogModel

class WaOutboundServiceTests(TestCase):
    @patch("contact.modules.gateways.whatsapp_cloud.application.services.wa_outbound_service.send_text")
    def test_send_safe_text_deduplicates(self, mock_send):
        mock_send.return_value = {"status": 200}
        to = "123"
        text = "hello"
        
        # First send
        resp1 = send_safe_text(to, text)
        self.assertEqual(resp1.get("status"), 200)
        self.assertTrue(mock_send.called)
        self.assertEqual(mock_send.call_count, 1)
        
        # Verify log created
        self.assertTrue(MessageEventLogModel.objects.filter(provider="whatsapp_cloud", direction="OUT").exists())
        
        # Second send (same day, same payload)
        resp2 = send_safe_text(to, text)
        self.assertEqual(resp2.get("status"), "skipped")
        self.assertEqual(resp2.get("reason"), "duplicate")
        self.assertEqual(mock_send.call_count, 1) # Should not be called again

    @patch("contact.modules.gateways.whatsapp_cloud.application.services.wa_outbound_service.send_product_list")
    def test_send_safe_product_list_deduplicates(self, mock_send):
        mock_send.return_value = {"status": 200}
        to = "123"
        cat = "cat1"
        rids = ["sku1", "sku2"]
        
        # First send
        resp1 = send_safe_product_list(to, cat, rids)
        self.assertEqual(resp1.get("status"), 200)
        self.assertEqual(mock_send.call_count, 1)
        
        # Second send
        resp2 = send_safe_product_list(to, cat, rids)
        self.assertEqual(resp2.get("status"), "skipped")
        self.assertEqual(mock_send.call_count, 1)
