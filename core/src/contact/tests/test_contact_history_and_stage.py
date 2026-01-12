from django.test import TestCase
from contact.modules.conversations.application.handlers.handle_whatsapp_inbound_h import execute as inbound
from contact.modules.contacts.application.commands.upsert_contact_fact_cmd import upsert_contact_fact_cmd
from contact.modules.conversations.infrastructure.orm.conversation_repo import get_by_contact_id
from contact.modules.conversations.domain.conversation_stage import ConversationStage
from contact.models import Contact
from contact.modules.contacts.infrastructure.orm.contact_history_models import ContactSkuStatModel


class ContactHistoryStageTests(TestCase):
    def setUp(self):
        self.whatsapp_id = "5491199999999"

    def test_profile_skips_e1(self):
        Contact.objects.create(
            whatsapp_id=self.whatsapp_id,
            name="",
            business_type="",
            type=Contact.TYPE_CLIENT,
            is_active=True,
        )
        c = Contact.objects.get(whatsapp_id=self.whatsapp_id)
        upsert_contact_fact_cmd(c.id, "name", "Juan Perez", source="USER", confidence=1.0)
        upsert_contact_fact_cmd(c.id, "zone", "CABA", source="USER", confidence=1.0)
        upsert_contact_fact_cmd(c.id, "business_type", "Kiosco", source="USER", confidence=1.0)

        out = inbound({"provider": "whatsapp", "provider_message_id": "m1", "whatsapp_id": self.whatsapp_id, "text": "Hola"})
        self.assertIn("Propuesta #", out)
        st = get_by_contact_id(c.id)
        self.assertEqual(st.stage, ConversationStage.E2_PROPOSAL.value)

    def test_stats_update_only_on_confirmed(self):
        Contact.objects.create(
            whatsapp_id=self.whatsapp_id,
            name="",
            business_type="",
            type=Contact.TYPE_CLIENT,
            is_active=True,
        )
        c = Contact.objects.get(whatsapp_id=self.whatsapp_id)
        upsert_contact_fact_cmd(c.id, "name", "Juan Perez", source="USER", confidence=1.0)
        upsert_contact_fact_cmd(c.id, "zone", "CABA", source="USER", confidence=1.0)
        upsert_contact_fact_cmd(c.id, "business_type", "Kiosco", source="USER", confidence=1.0)

        inbound({"provider": "whatsapp", "provider_message_id": "m2", "whatsapp_id": self.whatsapp_id, "text": "Hola"})
        self.assertFalse(ContactSkuStatModel.objects.filter(contact_id=c.id).exists())

        inbound({"provider": "whatsapp", "provider_message_id": "m3", "whatsapp_id": self.whatsapp_id, "text": "OK"})
        self.assertTrue(ContactSkuStatModel.objects.filter(contact_id=c.id).exists())

    def test_confirm_idempotent_does_not_double_stats(self):
        Contact.objects.create(
            whatsapp_id=self.whatsapp_id,
            name="",
            business_type="",
            type=Contact.TYPE_CLIENT,
            is_active=True,
        )
        c = Contact.objects.get(whatsapp_id=self.whatsapp_id)
        upsert_contact_fact_cmd(c.id, "name", "Juan Perez", source="USER", confidence=1.0)
        upsert_contact_fact_cmd(c.id, "zone", "CABA", source="USER", confidence=1.0)
        upsert_contact_fact_cmd(c.id, "business_type", "Kiosco", source="USER", confidence=1.0)

        inbound({"provider": "whatsapp", "provider_message_id": "m4", "whatsapp_id": self.whatsapp_id, "text": "Hola"})
        inbound({"provider": "whatsapp", "provider_message_id": "m5", "whatsapp_id": self.whatsapp_id, "text": "OK"})
        stats = list(ContactSkuStatModel.objects.filter(contact_id=c.id))
        total_first = sum(s.qty_total for s in stats)

        inbound({"provider": "whatsapp", "provider_message_id": "m6", "whatsapp_id": self.whatsapp_id, "text": "OK"})
        stats2 = list(ContactSkuStatModel.objects.filter(contact_id=c.id))
        total_second = sum(s.qty_total for s in stats2)
        self.assertEqual(total_first, total_second)
