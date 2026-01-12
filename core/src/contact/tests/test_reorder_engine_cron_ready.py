from django.test import TestCase
from datetime import date, timedelta, datetime
from unittest.mock import patch
from contact.models import Contact, OrderModel
from contact.modules.contacts.infrastructure.orm.contact_history_models import ContactReorderProfileModel
from contact.modules.reorder.application.commands.run_reorder_engine_cmd import execute as run_engine
from contact.modules.messaging.infrastructure.orm.message_event_models import MessageEventLogModel


class ReorderEngineCronReadyTests(TestCase):
    @patch("contact.modules.reorder.application.commands.run_reorder_engine_cmd.send_safe_product_list")
    @patch("contact.modules.reorder.application.commands.run_reorder_engine_cmd.send_safe_text")
    def test_due_contact_sends_once_and_updates_next_date(self, mock_text, mock_prod):
        c = Contact.objects.create(whatsapp_id="w10", name="X", business_type="K", type=Contact.TYPE_CLIENT, is_active=True)
        prof = ContactReorderProfileModel.objects.create(contact=c, status=ContactReorderProfileModel.STATUS_ACTIVE, cadence_days=5, next_reorder_date=date.today())
        mock_prod.return_value = {"status": 200}
        cnt = run_engine(apply=True, limit=10)
        self.assertEqual(cnt, 1)
        prof.refresh_from_db()
        self.assertEqual(prof.next_reorder_date, date.today() + timedelta(days=5))
        self.assertTrue(mock_prod.called or mock_text.called)

    @patch("contact.modules.reorder.application.commands.run_reorder_engine_cmd.send_safe_product_list")
    def test_rerun_same_day_dedupes(self, mock_prod):
        c = Contact.objects.create(whatsapp_id="w11", name="Y", business_type="K", type=Contact.TYPE_CLIENT, is_active=True)
        ContactReorderProfileModel.objects.create(contact=c, status=ContactReorderProfileModel.STATUS_ACTIVE, cadence_days=7, next_reorder_date=date.today())
        mock_prod.return_value = {"status": 200}
        cnt1 = run_engine(apply=True, limit=10)
        cnt2 = run_engine(apply=True, limit=10)
        self.assertEqual(cnt1, 1)
        self.assertEqual(cnt2, 0)
        # EventLog daily dedupe exists
        today_key = f"reorder:{c.id}:{date.today().strftime('%Y%m%d')}"
        self.assertTrue(MessageEventLogModel.objects.filter(provider="reorder_engine", external_event_id=today_key).exists())

    @patch("contact.modules.reorder.application.commands.run_reorder_engine_cmd.send_safe_product_list")
    @patch("contact.modules.reorder.application.commands.run_reorder_engine_cmd.send_safe_text")
    def test_skip_if_postpone_pending(self, mock_text, mock_prod):
        c = Contact.objects.create(whatsapp_id="w12", name="Z", business_type="K", type=Contact.TYPE_CLIENT, is_active=True)
        ContactReorderProfileModel.objects.create(contact=c, status=ContactReorderProfileModel.STATUS_ACTIVE, cadence_days=7, next_reorder_date=date.today(), postpone_status=ContactReorderProfileModel.POSTPONE_PENDING)
        cnt = run_engine(apply=True, limit=10)
        self.assertEqual(cnt, 0)
        mock_prod.assert_not_called()
        mock_text.assert_not_called()

    @patch("contact.modules.reorder.application.commands.run_reorder_engine_cmd.send_safe_product_list")
    @patch("contact.modules.reorder.application.commands.run_reorder_engine_cmd.send_safe_text")
    def test_skip_if_postpone_applied_future(self, mock_text, mock_prod):
        c = Contact.objects.create(whatsapp_id="w13", name="W", business_type="K", type=Contact.TYPE_CLIENT, is_active=True)
        ContactReorderProfileModel.objects.create(contact=c, status=ContactReorderProfileModel.STATUS_ACTIVE, cadence_days=7, next_reorder_date=date.today(), postpone_status=ContactReorderProfileModel.POSTPONE_APPLIED, postpone_until_dt=datetime.now() + timedelta(days=1))
        cnt = run_engine(apply=True, limit=10)
        self.assertEqual(cnt, 0)
        mock_prod.assert_not_called()
        mock_text.assert_not_called()

    @patch("contact.modules.reorder.application.commands.run_reorder_engine_cmd.get_summary")
    @patch("contact.modules.reorder.application.commands.run_reorder_engine_cmd.send_safe_product_list")
    @patch("contact.modules.reorder.application.commands.run_reorder_engine_cmd.send_safe_text")
    def test_send_product_list_empty_does_not_send_and_logs_failed(self, mock_text, mock_prod, mock_summary):
        # Simulate create_order creating empty template by making send_product_list called with empty SKUs
        c = Contact.objects.create(whatsapp_id="w14", name="V", business_type="K", type=Contact.TYPE_CLIENT, is_active=True)
        ContactReorderProfileModel.objects.create(contact=c, status=ContactReorderProfileModel.STATUS_ACTIVE, cadence_days=7, next_reorder_date=date.today())
        
        mock_prod.side_effect = AssertionError("should not be called on empty catalog")
        mock_summary.return_value = {"items": [], "text": ""}
        
        cnt = run_engine(apply=True, limit=10)
        
        self.assertEqual(cnt, 1)
        mock_text.assert_called_once()
        args, kwargs = mock_text.call_args
        self.assertIn("No pude armar tu reposición", args[1])
        self.assertEqual(kwargs.get("meta"), {"error": "FAILED_EMPTY_CATALOG"})

    @patch("contact.modules.reorder.application.commands.run_reorder_engine_cmd.get_summary")
    @patch("contact.modules.gateways.whatsapp_cloud.application.services.wa_outbound_service.send_product_list")
    def test_existing_customer_sets_proposal_source_base_from_history(self, mock_prod, mock_summary):
        # DoD C: Existing customer -> BASE_FROM_HISTORY
        c = Contact.objects.create(whatsapp_id="w_existing", name="E", business_type="K", type=Contact.TYPE_CLIENT, is_active=True)
        ContactReorderProfileModel.objects.create(contact=c, status=ContactReorderProfileModel.STATUS_ACTIVE, cadence_days=7, next_reorder_date=date.today())
        
        # Create a COMPLETED order in history
        OrderModel.objects.create(contact=c, status="COMPLETED")
        
        mock_summary.return_value = {"items": [{"product_ref": "SKU:P1", "qty": 1}], "text": ""}
        mock_prod.return_value = {"status": 200}
        run_engine(apply=True, limit=10)
        out = MessageEventLogModel.objects.filter(direction="OUT", provider="whatsapp_cloud").latest("id")
        self.assertEqual(out.payload_json.get("proposal_source"), "BASE_FROM_HISTORY")
        self.assertEqual(out.payload_json.get("skus_count"), 1)
        self.assertEqual(out.payload_json.get("contact_id"), c.id)

    @patch("contact.modules.reorder.application.commands.run_reorder_engine_cmd.get_summary")
    @patch("contact.modules.gateways.whatsapp_cloud.application.services.wa_outbound_service.send_product_list")
    def test_new_customer_sets_proposal_source_new_template(self, mock_prod, mock_summary):
        # DoD C: New customer (no history) -> NEW_TEMPLATE
        c = Contact.objects.create(whatsapp_id="w_new", name="N", business_type="K", type=Contact.TYPE_CLIENT, is_active=True)
        ContactReorderProfileModel.objects.create(contact=c, status=ContactReorderProfileModel.STATUS_ACTIVE, cadence_days=7, next_reorder_date=date.today())
        
        # NO completed orders
        
        mock_summary.return_value = {"items": [{"product_ref": "SKU:P1", "qty": 1}], "text": ""}
        mock_prod.return_value = {"status": 200}
        run_engine(apply=True, limit=10)
        out = MessageEventLogModel.objects.filter(direction="OUT", provider="whatsapp_cloud").latest("id")
        self.assertEqual(out.payload_json.get("proposal_source"), "NEW_TEMPLATE")
        self.assertEqual(out.payload_json.get("skus_count"), 1)
        self.assertEqual(out.payload_json.get("contact_id"), c.id)
        self.assertEqual(out.payload_json.get("list_code"), "kiosk_base")

    @patch("contact.modules.reorder.application.commands.run_reorder_engine_cmd.get_summary")
    @patch("contact.modules.gateways.whatsapp_cloud.application.services.wa_outbound_service.send_product_list")
    def test_existing_customer_uses_history_source_and_logs_it(self, mock_prod, mock_summary):
        c = Contact.objects.create(whatsapp_id="w_hist", name="H", business_type="K", type=Contact.TYPE_CLIENT, is_active=True)
        ContactReorderProfileModel.objects.create(contact=c, status=ContactReorderProfileModel.STATUS_ACTIVE, cadence_days=7, next_reorder_date=date.today())
        OrderModel.objects.create(contact=c, status="COMPLETED")
        mock_summary.return_value = {"items": [{"product_ref": "SKU:P1", "qty": 1}], "text": ""}
        mock_prod.return_value = {"status": 200}
        run_engine(apply=True, limit=10)
        out = MessageEventLogModel.objects.filter(direction="OUT", provider="whatsapp_cloud").latest("id")
        self.assertEqual(out.payload_json.get("proposal_source"), "BASE_FROM_HISTORY")
        self.assertEqual(out.payload_json.get("skus_count"), 1)
        self.assertEqual(out.payload_json.get("contact_id"), c.id)
        self.assertIsNone(out.payload_json.get("list_code"))

    @patch("contact.modules.reorder.application.commands.run_reorder_engine_cmd.get_summary")
    @patch("contact.modules.gateways.whatsapp_cloud.application.services.wa_outbound_service.send_product_list")
    def test_new_customer_uses_template_source_and_logs_it(self, mock_prod, mock_summary):
        c = Contact.objects.create(whatsapp_id="w_temp", name="T", business_type="K", type=Contact.TYPE_CLIENT, is_active=True)
        ContactReorderProfileModel.objects.create(contact=c, status=ContactReorderProfileModel.STATUS_ACTIVE, cadence_days=7, next_reorder_date=date.today(), default_list_code="kiosk_base")
        mock_summary.return_value = {"items": [{"product_ref": "SKU:P1", "qty": 1}], "text": ""}
        mock_prod.return_value = {"status": 200}
        run_engine(apply=True, limit=10)
        out = MessageEventLogModel.objects.filter(direction="OUT", provider="whatsapp_cloud").latest("id")
        self.assertEqual(out.payload_json.get("proposal_source"), "NEW_TEMPLATE")
        self.assertEqual(out.payload_json.get("list_code"), "kiosk_base")
        self.assertEqual(out.payload_json.get("skus_count"), 1)
        self.assertEqual(out.payload_json.get("contact_id"), c.id)
