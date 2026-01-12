from django.test import TestCase
from contact.modules.messaging.infrastructure.orm.message_event_repo import log_outbound
from contact.modules.messaging.infrastructure.orm.message_event_models import MessageEventLogModel


class EventLogOutboundIdempotencyTests(TestCase):
    def test_outbound_dup_by_echo_id_is_single(self):
        provider = "chatwoot"
        echo_id = "e1"
        conversation_external_id = "c1"
        payload = {"k": "v"}
        log_outbound(provider, echo_id, conversation_external_id, None, "SENT", payload)
        log_outbound(provider, echo_id, conversation_external_id, None, "FAILED", payload)
        cnt = MessageEventLogModel.objects.filter(provider=provider, echo_id=echo_id).count()
        self.assertEqual(cnt, 1)
