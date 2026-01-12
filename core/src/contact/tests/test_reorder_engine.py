from django.test import TestCase
from datetime import date, timedelta
from contact.models import Contact, OrderModel
from contact.modules.contacts.infrastructure.orm.contact_history_models import ContactReorderProfileModel
from contact.modules.reorder.application.commands.run_reorder_engine_cmd import execute as run_engine
from unittest.mock import patch


class ReorderEngineTests(TestCase):
    @patch("contact.modules.reorder.application.commands.run_reorder_engine_cmd.send_safe_product_list")
    @patch("contact.modules.reorder.application.commands.run_reorder_engine_cmd.send_safe_text")
    def test_skips_if_proposed_exists(self, mock_text, mock_prod):
        c = Contact.objects.create(whatsapp_id="w1", name="A", business_type="K", type=Contact.TYPE_CLIENT, is_active=True)
        ContactReorderProfileModel.objects.create(contact=c, status=ContactReorderProfileModel.STATUS_ACTIVE, cadence_days=7, next_reorder_date=date.today())
        OrderModel.objects.create(contact=c, status="PROPOSED")
        cnt = run_engine(apply=True)
        self.assertEqual(cnt, 0)
        mock_prod.assert_not_called()
        mock_text.assert_not_called()

    @patch("contact.modules.reorder.application.commands.run_reorder_engine_cmd.send_safe_product_list")
    @patch("contact.modules.reorder.application.commands.run_reorder_engine_cmd.send_safe_text")
    def test_creates_and_sends_when_due(self, mock_text, mock_prod):
        c = Contact.objects.create(whatsapp_id="w2", name="B", business_type="K", type=Contact.TYPE_CLIENT, is_active=True)
        ContactReorderProfileModel.objects.create(contact=c, status=ContactReorderProfileModel.STATUS_ACTIVE, cadence_days=7, next_reorder_date=date.today())
        
        cnt = run_engine(apply=True)
        self.assertEqual(cnt, 1)
        self.assertTrue(mock_text.called or mock_prod.called)

    @patch("contact.modules.reorder.application.commands.run_reorder_engine_cmd.send_safe_product_list")
    @patch("contact.modules.reorder.application.commands.run_reorder_engine_cmd.send_safe_text")
    def test_updates_next_reorder_date(self, mock_text, mock_prod):
        c = Contact.objects.create(whatsapp_id="w3", name="C", business_type="K", type=Contact.TYPE_CLIENT, is_active=True)
        prof = ContactReorderProfileModel.objects.create(contact=c, status=ContactReorderProfileModel.STATUS_ACTIVE, cadence_days=10, next_reorder_date=date.today())
        run_engine(apply=True)
        prof.refresh_from_db()
        self.assertEqual(prof.next_reorder_date, date.today() + timedelta(days=10))
