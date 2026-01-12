from django.test import TestCase
from contact.modules.messaging.infrastructure.orm.message_event_repo import log_inbound
from contact.modules.messaging.infrastructure.orm.message_event_models import MessageEventLogModel


class EventLogInboundIdempotencyTests(TestCase):
    def test_inbound_dup_by_external_event_id_is_single(self):
        provider = "chatwoot"
        external_event_id = "ev1"
        conversation_external_id = "c1"
        payload = {"k": "v"}
        log_inbound(provider, external_event_id, conversation_external_id, None, "RECEIVED", payload)
        log_inbound(provider, external_event_id, conversation_external_id, None, "PROCESSED", payload)
        cnt = MessageEventLogModel.objects.filter(provider=provider, external_event_id=external_event_id).count()
        self.assertEqual(cnt, 1)
