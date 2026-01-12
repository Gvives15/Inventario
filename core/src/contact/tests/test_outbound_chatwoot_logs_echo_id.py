from django.test import TestCase
from unittest.mock import patch
from contact.modules.gateways.chatwoot.application.handlers.send_chatwoot_message_h import execute as send_msg
from contact.modules.messaging.infrastructure.orm.message_event_models import MessageEventLogModel


class OutboundChatwootTests(TestCase):
    @patch("contact.modules.gateways.chatwoot.infrastructure.chatwoot_client.send_message")
    def test_logs_echo_id(self, mock_send):
        mock_send.return_value = {"status": 200, "body": "{}"}
        r = send_msg("conv-1", "Hola")
        self.assertEqual(r, "OK")
        obj = MessageEventLogModel.objects.filter(provider="chatwoot").first()
        self.assertIsNotNone(obj)
        self.assertEqual(obj.direction, "OUT")
        self.assertIsNotNone(obj.echo_id)
